from rest_framework import viewsets
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient
from rest_framework.response import Response
from django.http import HttpResponse
from databaseServer.models import Provider, CloudService, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications, ComputeSpecifications


class ViewHello(viewsets.ViewSet):

    # Define a custom action named 'hello'
    def list(self, request):
        return Response("hello")


def compute_fetch_view(request):
    # Get the Provider object for 'Azure'
    azure_provider = Provider.objects.get(name='Azure')

    # Get CloudService objects for 'Compute' type under 'Azure'
    compute_services = CloudService.objects.filter(service_type='Compute', provider=azure_provider)

    # Delete only ComputeSpecifications entries that are related to the 'Compute' CloudService under 'Azure'
    ComputeSpecifications.objects.filter(cloud_service__in=compute_services).delete()

    subscription_id = "677918b9-22da-46ac-abd1-1fb1807ebaef"  # Replace with your actual subscription ID
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    subscription_client = SubscriptionClient(credential)
    prices_api_url = "https://prices.azure.com/api/retail/prices"

    # Fetch retail prices
    def get_retail_prices():
        filter_query = "serviceName eq 'Virtual Machines'"
        prices_response = requests.get(prices_api_url, params={'$filter': filter_query})
        if prices_response.status_code == 200:
            return {item['armSkuName']: item for item in prices_response.json()['Items']}
        else:
            raise Exception(f"Failed to fetch prices: {prices_response.status_code}")

    supported_regions = [
        'eastus', 'eastus2', 'westus', 'centralus', 'northcentralus', 'southcentralus',
        'northeurope', 'westeurope', 'eastasia', 'southeastasia', 'japaneast', 'japanwest',
        'australiaeast', 'australiasoutheast', 'australiacentral', 'brazilsouth',
        'southindia', 'centralindia', 'westindia', 'canadacentral', 'canadaeast',
        'westus2', 'westcentralus', 'uksouth', 'ukwest', 'koreacentral', 'koreasouth',
        'francecentral', 'southafricanorth', 'uaenorth', 'switzerlandnorth',
        'germanywestcentral', 'norwayeast', 'jioindiawest', 'westus3', 'swedencentral',
        'qatarcentral', 'polandcentral', 'italynorth', 'israelcentral'
    ]
    regions = [location.name for location in subscription_client.subscriptions.list_locations(subscription_id)]
    retail_prices = get_retail_prices()

    provider, _ = Provider.objects.get_or_create(name="Azure")
    cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type="Compute", defaults={'description': 'Azure Compute Service'})

    for region in regions:
        if region not in supported_regions:
            continue  # Skip unsupported regions

        vm_sizes = compute_client.virtual_machine_sizes.list(location=region)
        for vm_size in vm_sizes:
            price_info = retail_prices.get(vm_size.name)

            if price_info and 'retailPrice' in price_info:
                unit_price = price_info['retailPrice']
                monthly_price = round(unit_price * 730, 2)  # Assuming 730 hours in a month for price calculation
                cpu_label = "vCPU" if vm_size.number_of_cores == 1 else "vCPUs"

                ComputeSpecifications.objects.update_or_create(
                    sku=vm_size.name,
                    defaults={
                        'name': price_info.get('productName', 'Unknown'),
                        'provider': provider,
                        'cloud_service': cloud_service,
                        'instance_type': vm_size.name,
                        'operating_system': 'Not specified',  # Set your desired default value
                        'cpu': f"{vm_size.number_of_cores} {cpu_label}",
                        'memory': f"{vm_size.memory_in_mb / 1024} GiB",
                        'network_performance': 'Not specified',  # Set your desired default value
                        'region': region,
                        'unit_price': str(unit_price),
                        'currency': 'USD',  # Assuming USD, change if necessary
                        'price_monthly': str(monthly_price)
                    }
                )

    return HttpResponse("Data fetched and stored successfully")


# Azure storage fetch
def storage_fetch_view(request):
    # Get the Provider object for 'Azure'
    azure_provider = Provider.objects.get(name='Azure')

    # Get CloudService objects for 'Storage' type under 'Azure'
    storage_services = CloudService.objects.filter(service_type='Storage', provider=azure_provider)

    # Delete only StorageSpecifications entries that are related to the 'Storage' CloudService under 'Azure'
    StorageSpecifications.objects.filter(cloud_service__in=storage_services).delete()

    api_url = "https://prices.azure.com/api/retail/prices"
    query_params = {
        '$filter': "serviceName eq 'Storage'",
        'currency': 'USD'  # Specify the currency as USD
    }
    response = requests.get(api_url, params=query_params)

    if response.status_code == 200:
        data = response.json()
        items = data.get('Items', [])

        # Get or create the Provider object with the hardcoded name
        provider_name = 'Azure'  # Update this with the desired provider name
        provider, _ = Provider.objects.get_or_create(name=provider_name)

        # Get the CloudService object representing the storage service
        cloud_service_type = 'Storage'  # Assuming 'Storage' is the service_type for storage-related services
        cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type=cloud_service_type)

        for item in items:
            StorageSpecifications.objects.create(
                name=item.get('productName'),
                provider=provider,
                cloud_service=cloud_service,
                sku=item.get('skuName'),
                unit_price=item.get('retailPrice'),
                unit_of_storage=item.get('unitOfMeasure'),
                region=item.get('armRegionName', 'No region provided')  # Providing default value
            )
        return HttpResponse("Data fetched and stored successfully.")
    else:
        return HttpResponse(f"Failed to fetch data from Azure. Status code: {response.status_code}")


# Azure networking fetch
def networking_fetch_view(request):
    # Get the Provider object for 'Azure'
    azure_provider = Provider.objects.get(name='Azure')

    # Get CloudService objects for 'Networking' type under 'Azure'
    networking_services = CloudService.objects.filter(service_type='Networking', provider=azure_provider)

    # Delete only NetworkingSpecifications entries that are related to the 'Networking' CloudService under 'Azure'
    NetworkingSpecifications.objects.filter(cloud_service__in=networking_services).delete()

    # Function to fetch Azure pricing data for a specific service name
    def fetch_azure_pricing(service_name):
        api_url = "https://prices.azure.com/api/retail/prices"
        resolution = []
        take = 0

        while True:
            params = {
            "$filter": f"serviceName eq '{service_name}'",
            "$skip": take,
            "currency": "USD"  # Specify the currency as USD
        }

            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                basket = data.get('Items', [])
                if not basket:
                    break
                resolution += basket
                take += len(basket)
            else:
                print(f"Hail, the work found some jolt: {response.status_code}")
                break

        return resolution

    # Function to store fetched pricing data in the database
    def store_pricing_data(pricing_data):
        provider_name = 'Azure'
        provider, _ = Provider.objects.get_or_create(name=provider_name)

        # Get or create CloudService object representing networking service
        cloud_service_type = 'Networking'  # Update with correct service type
        cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type=cloud_service_type)

        for service in pricing_data:
            name_with_region = f"{service.get('productName', 'N/A')} - {service.get('armRegionName', 'Global')}"
            NetworkingSpecifications.objects.create(
                name=name_with_region,
                provider=provider,
                cloud_service=cloud_service,
                sku=service.get('skuName', 'N/A'),
                unit_price=service.get('retailPrice', '0.0'),
                unit_of_measure=service.get('unitOfMeasure', 'N/A'),
                region=service.get('armRegionName', 'No region provided')
            )

    # Fetch pricing data for networking services
    service_names = ["Content Delivery Network", "DNS", "Azure DNS"]  # Update with desired service names
    for service_name in service_names:
        print(f"Fetching pricing data for: {service_name}")
        pricing_data = fetch_azure_pricing(service_name)
        store_pricing_data(pricing_data)

    return HttpResponse("Networking pricing data fetched and stored successfully.")



# Azure database fetch
def database_fetch_view(request):
    # Get the Provider object for 'Azure'
    azure_provider = Provider.objects.get(name='Azure')

    # Get CloudService objects for 'Database' type under 'Azure'
    database_services = CloudService.objects.filter(service_type='Database', provider=azure_provider)

    # Delete only DatabaseSpecifications entries that are related to the 'Database' CloudService under 'Azure'
    DatabaseSpecifications.objects.filter(cloud_service__in=database_services).delete()


    def fetch_azure_database_pricing(region='eastus'):
        api_url = "https://prices.azure.com/api/retail/prices"
        resolution = []
        take = 0

        while True:
            params = {
                "$filter": "serviceFamily eq 'Databases'",
                "$skip": take
            }

            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                basket = data.get('Items', [])
                if not basket:
                    break
                resolution += basket
                take += len(basket)
            else:
                print(f"Failed to fetch pricing data: {response.status_code}")
                break

        # Filter the fetched data based on the specified region
        filtered_data = [item for item in resolution if item.get('armRegionName') == region]
        return filtered_data


    def store_database_pricing_data(database_pricing_data):
        provider_name = 'Azure'
        provider, _ = Provider.objects.get_or_create(name=provider_name)

        cloud_service_type = 'Database'  # Assuming 'Database' is the service_type for database-related services
        cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type=cloud_service_type)

        for service in database_pricing_data:
            database_type = service.get('serviceName', 'Unknown Database')
            DatabaseSpecifications.objects.create(
                name=service.get('productName', 'N/A'),
                provider=provider,
                cloud_service=cloud_service,
                data_type=database_type,
                sku=service.get('skuName', 'N/A'),
                unit_price=service.get('retailPrice', '0.0'),
                unit_of_storage=service.get('unitOfMeasure', 'N/A'),
                region=service.get('armRegionName', 'No region provided')
            )

    # Fetch pricing data for database services
    database_pricing_data = fetch_azure_database_pricing()
    store_database_pricing_data(database_pricing_data)

    return HttpResponse("Database pricing data fetched and stored successfully.")


###################################################################################################
###################################################################################################
###################################################################################################
############################ The backend logic for advanced form ##################################
###################################################################################################
###################################################################################################
###################################################################################################
def calculated_data_Azure(monthly_budget, expected_ram, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    computed_data = {'provider': 'Microsoft Azure'}  # Initialize dictionary to store computed data

    # Mapping of user-friendly RAM/CPU options to SKU
    ram_to_sku_mapping = {
        '1vCPU': 'Standard_D1_v2',  # Example mapping, adjust based on actual data
        '2vCPUs': 'Standard_B2als_v2',  # Example mapping, adjust based on actual data
        '4vCPUs': 'Standard_D4_v4',  # Example mapping
        '8vCPUs': 'Standard_D8s_v5',  # Example mapping
        '16vCPUs': 'Standard_D16ds_v5',  # Example mapping
        # add mappings as necessary
    }

    # Retrieve the SKU from the mapping based on the expected_ram
    expected_sku = ram_to_sku_mapping.get(expected_ram)

    # Retrieve data from the database based on the provided SKU and location
    if expected_sku:
        compute_instance = ComputeSpecifications.objects.filter(sku=expected_sku).first()
        if compute_instance:
            computed_data['compute'] = {
                'name': compute_instance.name,
                'unit_price': compute_instance.price_monthly,
                'cpu': compute_instance.cpu,
                'memory': compute_instance.memory,
                'sku': compute_instance.sku,
                'provider': compute_instance.provider.name,
                'cloud_service': compute_instance.cloud_service.service_type,
                'price_monthly': compute_instance.price_monthly
            }

        # Define size to price multiplier mapping
    size_multiplier_mapping = {
        'small': 10,
        'medium': 100,
        'large': 1000,
        'noDatabase': 0,
    }

    # Define name and SKU mapping with primary and secondary options
    service_to_name_and_sku_mapping = {
        'noSQL': {
            'primary': {'name': 'Azure Cosmos DB for MongoDB vCore', 'sku': 'General Purpose Storage'},
            'secondary': {'name': 'Azure Cosmos DB', 'sku': 'mRUs'}  # Adjust as needed
        },
        'sql': {
            'primary': {'name': 'SQL Database Standard - Storage', 'sku': 'Standard'},
            'secondary': {'name': 'SQL Database Premium - Storage', 'sku': 'Premium'}  # Adjust as needed
        },
        'noDatabase': {
            'primary': {'name': '', 'sku': ''},
            'secondary': {'name': '', 'sku': ''}  # Adjust as needed
        }
    }

    service_info = service_to_name_and_sku_mapping.get(database_service)

    if service_info:
        # Attempt to fetch the primary database instance
        database_instance = DatabaseSpecifications.objects.filter(
            name=service_info['primary']['name'],
            sku=service_info['primary']['sku']
        ).first()

        # If not found, try the secondary option
        if not database_instance:
            database_instance = DatabaseSpecifications.objects.filter(
                name=service_info['secondary']['name'],
                sku=service_info['secondary']['sku']
            ).first()

        if database_instance:
            # Calculate the unit price based on the selected database size
            size_multiplier = size_multiplier_mapping.get(database_size, 1)
            unit_price = float(database_instance.unit_price) * size_multiplier

            computed_data['database'] = {
                'name': database_instance.name,
                'unit_price': f'{unit_price:.2f}',
                'sku': database_instance.sku,
                'data_type': database_instance.data_type,
                'provider': database_instance.provider.name,
                'cloud_service': database_instance.cloud_service.service_type
            }
        else:
            computed_data['database'] = 'No matching database found'

    # Define size to price multiplier mapping, adjust as needed
    size_multiplier_mapping_storage = {
        'small': 1024,
        'medium': 10240,
        'large': 102400,
        'notSure': 0,
    }

    # Define storage type to name and SKU mapping with primary and secondary options
    storage_to_name_and_sku_mapping_storage = {
        'Object Storage': {
            'primary': {'name': 'General Block Blob', 'sku': 'Standard GRS'},
            'secondary': {'name': 'General Block Blob v2', 'sku': 'Hot GRS'}
        },
        'File Storage': {
            'primary': {'name': 'Files v2', 'sku': 'Cool LRS'},
            'secondary': {'name': 'Files', 'sku': 'Standard LRS'}
        },
        'Block Storage': {
            'primary': {'name': 'Standard SSD Managed Disks', 'sku': 'E70 LRS'},
            'secondary': {'name': 'Premium SSD Managed Disks', 'sku': 'P15 LRS'}
        },
        'No Storage': {
            'primary': {'name': '', 'sku': ''},
            'secondary': {'name': '', 'sku': ''}  # Adjust as needed
        }
        # Add more mappings as necessary for different storage types
    }

    storage_info = storage_to_name_and_sku_mapping_storage.get(cloud_storage)

    if storage_info:
        # Attempt to fetch the primary storage instance
        storage_instance = StorageSpecifications.objects.filter(
            name=storage_info['primary']['name'],
            sku=storage_info['primary']['sku']
        ).first()

        # If not found, try the secondary option
        if not storage_instance:
            storage_instance = StorageSpecifications.objects.filter(
                name=storage_info['secondary']['name'],
                sku=storage_info['secondary']['sku']
            ).first()

        if storage_instance:
            # Calculate the base unit price
            unit_price = float(storage_instance.unit_price)

            # Interpret unit of storage to calculate monthly price
            unit_of_storage = storage_instance.unit_of_storage.lower()
            if 'gb/month' in unit_of_storage or '1/month' in unit_of_storage:
                base_price = unit_price  # Already monthly price
            elif '10k/month' in unit_of_storage or '10k' in unit_of_storage:
                base_price = unit_price * 10000  # Example, adjust according to your pricing model
            else:
                base_price = unit_price  # Default case, adjust as needed

            # Apply size multiplier based on storage size selected by user
            size_multiplier = size_multiplier_mapping_storage.get(storage_size, 1)
            price_monthly = base_price * size_multiplier

            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': f'{price_monthly:.2f}',  # Per unit price
                'price_monthly': f'{price_monthly:.2f}',  # Total monthly price based on size
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type,
                'unit_of_storage': storage_instance.unit_of_storage
            }
        else:
            computed_data['storage'] = 'No matching storage found'



    # if networking_feature:
    #     if 'Content' in networking_feature:
    #         # Query for the first networking instance based on the keyword "CDN"
    #         networking_instance = NetworkingSpecifications.objects.filter(name__icontains='CDN').first()
    #     else:
    #         # Query for the first networking instance based on the first word
    #         first_word = networking_feature.split()[0]
    #         networking_instance = NetworkingSpecifications.objects.filter(name__icontains=first_word).first()

    #     if networking_instance:
    #         computed_data['networking'] = {
    #             'name': networking_instance.name,
    #             'unit_price': networking_instance.unit_price,
    #             'unit_of_measure': networking_instance.unit_of_measure,
    #             'sku': networking_instance.sku,
    #             'provider': networking_instance.provider.name,
    #             'cloud_service': networking_instance.cloud_service.service_type
    #         }

    return computed_data


def calculated_data_Azure_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    computed_data = {'provider': 'Microsoft Azure',}  # Initialize dictionary to store computed data

    # Retrieve data from the database based on the provided keyword
    if expected_cpu:
        # Query for the first compute instance
        compute_instance = ComputeSpecifications.objects.filter(cpu=expected_cpu).first()
        if compute_instance:
            computed_data['compute'] = {
                'name': compute_instance.name,
                'unit_price': compute_instance.unit_price,
                'cpu': compute_instance.cpu,
                'memory': compute_instance.memory,
                'sku': compute_instance.sku,
                'provider': compute_instance.provider.name,
                'cloud_service': compute_instance.cloud_service.service_type
            }

    if cloud_storage:
        # Query for the first storage instance based on the keyword "File"
        storage_instance = StorageSpecifications.objects.filter(name__icontains='File').first()
        if storage_instance:
            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': storage_instance.unit_price,
                'unit_of_storage': storage_instance.unit_of_storage,
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type
            }

    if database_service:
        # Query for the first database instance
        database_instance = DatabaseSpecifications.objects.filter(name__icontains=database_service).first()
        if database_instance:
            computed_data['database'] = {
                'name': database_instance.name,
                'unit_price': database_instance.unit_price,
                'unit_of_storage': database_instance.unit_of_storage,
                'sku': database_instance.sku,
                'data_type': database_instance.data_type,
                'provider': database_instance.provider.name,
                'cloud_service': database_instance.cloud_service.service_type
            }
        else:
            computed_data['database'] = None

    if networking_feature:
        if 'Content' in networking_feature:
            # Query for the first networking instance based on the keyword "CDN"
            networking_instance = NetworkingSpecifications.objects.filter(name__icontains='CDN').first()
        else:
            # Query for the first networking instance based on the first word
            first_word = networking_feature.split()[0]
            networking_instance = NetworkingSpecifications.objects.filter(name__icontains=first_word).first()

        if networking_instance:
            computed_data['networking'] = {
                'name': networking_instance.name,
                'unit_price': networking_instance.unit_price,
                'unit_of_measure': networking_instance.unit_of_measure,
                'sku': networking_instance.sku,
                'provider': networking_instance.provider.name,
                'cloud_service': networking_instance.cloud_service.service_type
            }

    return computed_data