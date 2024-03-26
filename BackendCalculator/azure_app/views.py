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
    compute_price = 0.0;
    storage_pice = 0.0;
    database_price = 0.0;
    dns_price = 0.0
    cdn_price = 0.0
    monthly = 0.0;
    annual = 0.0;

    # Mapping of user-friendly RAM/CPU options to SKU
    ram_to_sku_mapping = {
        '1vCPU': 'Standard_D1',  # Example mapping, adjust based on actual data
        '2vCPUs': 'Standard_F2',  # Example mapping, adjust based on actual data
        '4vCPUs': 'Standard_D4ds_v4',  # Example mapping
        '8vCPUs': 'Standard_D8ps_v5',  # Example mapping
        '16vCPUs': 'Standard_B16as_v2',  # Example mapping
        # add mappings as necessary
    }

    # Retrieve the SKU from the mapping based on the expected_ram
    expected_sku = ram_to_sku_mapping.get(expected_ram)

        # Retrieve data from the database based on the provided SKU and location
    if expected_sku:
        compute_instance = ComputeSpecifications.objects.filter(sku=expected_sku).first()
        if compute_instance:
            # Base instance name with location
            base_name_with_location = f"{compute_instance.name} [US East (N. Virginia)]"

            # Append '+ Azure Standard Load Balancer' if scalability is essential
            if scalability == 'essential':
                instance_name = f"{base_name_with_location} + Azure Standard Load Balancer"
            else:
                instance_name = base_name_with_location

            compute_price = float(compute_instance.price_monthly)

            computed_data['compute'] = {
                'name': instance_name,
                'unit_price': compute_instance.price_monthly,
                'cpu': compute_instance.cpu,
                'memory': compute_instance.memory,
                'sku': compute_instance.sku,
                'provider': compute_instance.provider.name,
                'cloud_service': compute_instance.cloud_service.service_type,
                'price_monthly': compute_instance.price_monthly,
                'created_at': compute_instance.created_at.isoformat() if compute_instance.created_at else None,
            }

    # Assuming these are price multipliers for different service tiers or capacities
    size_multiplier_mapping = {
        'small': 10,    # 1 TB
        'medium': 100,  # 10 TB
        'large': 1000,  # 100 TB
        'noDatabase': 0,
    }

    service_to_name_and_sku_mapping = {
        'noSQL': {
            'primary': {
                'name': 'Azure Cosmos DB',
                'sku': 'RUm',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            },
            'secondary': {
                'name': 'Azure Cosmos DB for MongoDB vCore',
                'sku': 'General Purpose Storage',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            }
        },
        'sql': {
            'secondary': {
                'name': 'SQL Database Standard - Storage',
                'sku': 'Standard',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            },
            'primary': {
                'name': 'SQL Database Premium - Storage',
                'sku': 'Premium',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            }
        },
        'noDatabase': {
            'primary': {
                'name': '',
                'sku': '',
                'region': '',
                'unit_of_storage': ''
            },
            'secondary': {
                'name': '',
                'sku': '',
                'region': '',
                'unit_of_storage': ''
            }
        }
    }

    service_info = service_to_name_and_sku_mapping.get(database_service)

    if service_info:
        database_instance = DatabaseSpecifications.objects.filter(
            name=service_info['primary']['name'],
            sku=service_info['primary']['sku'],
            region=service_info['primary']['region'],
            unit_of_storage=service_info['primary']['unit_of_storage']
        ).first()

        if not database_instance:
            database_instance = DatabaseSpecifications.objects.filter(
                name=service_info['secondary']['name'],
                sku=service_info['secondary']['sku'],
                region=service_info['secondary']['region'],
                unit_of_storage=service_info['secondary']['unit_of_storage']
            ).first()

        if database_instance:
            size_multiplier = size_multiplier_mapping.get(database_size, 1)
            unit_price = float(database_instance.unit_price)  # Assume this gives price per GB/Month
            # Calculate the price for the selected size
            total_price = unit_price  * size_multiplier  # Assuming price needs to be calculated per TB
            database_price = float(total_price)

            computed_data['database'] = {
                'name': database_instance.name,
                'unit_price': f'{total_price:.2f}',
                'total_price': f'{total_price:.2f}',
                'sku': database_instance.sku,
                'region': database_instance.region,
                'unit_of_storage': database_instance.unit_of_storage,
                'data_type': database_instance.data_type,
                'provider': database_instance.provider.name,
                'cloud_service': database_instance.cloud_service.service_type,
                'created_at': database_instance.created_at.isoformat() if database_instance.created_at else None,
            }
        else:
            computed_data['database'] = 'No matching database found'
    else:
        computed_data['database'] = 'Service not found'

    # Define size to price multiplier mapping, adjust as needed
    size_multiplier_mapping_storage = {
        'small': 10,      # For 1 TB
        'medium': 100,    # For 10 TB
        'large': 1000,    # For 100 TB
        'notSure': 1,    # Default or unsure case
    }

        # Define storage type to name, SKU, region, and unit of storage mapping with primary and secondary options
    storage_to_name_and_sku_mapping_storage = {
        'Object Storage': {
            'primary': {'name': 'General Block Blob', 'sku': 'Standard GRS', 'region': 'uksouth', 'unit_of_storage': '1 GB/Month'},
            'secondary': {'name': 'General Block Blob v2', 'sku': 'Cold RA-GZRS', 'region': 'uksouth', 'unit_of_storage': '1 GB'}
        },
        'File Storage': {
            'primary': {'name': 'Files', 'sku': 'Standard LRS', 'region': 'brazilsoutheast', 'unit_of_storage': '1 GB/Month'},
            'secondary': {'name': 'Files v2', 'sku': 'Cool GRS', 'region': 'westeurope', 'unit_of_storage': '1 GB'}
        },
        'Block Storage': {
            'primary': {'name': 'Standard SSD Managed Disks', 'sku': 'E3 LRS', 'region': 'attnewyork1', 'unit_of_storage': '1/Month'},
            'secondary': {'name': 'Standard SSD Managed Disks', 'sku': 'E3 LRS', 'region': 'norwaywest', 'unit_of_storage': '1/Month'}
        },
        'No Storage': {
            'primary': {'name': '', 'sku': '', 'region': '', 'unit_of_storage': ''},
            'secondary': {'name': '', 'sku': '', 'region': '', 'unit_of_storage': ''}  # Adjust as needed
        }
        # Add more mappings as necessary for different storage types
    }

    storage_info = storage_to_name_and_sku_mapping_storage.get(cloud_storage)

    if storage_info:
        # Attempt to fetch the primary storage instance
        storage_instance = StorageSpecifications.objects.filter(
            name=storage_info['primary']['name'],
            sku=storage_info['primary']['sku'],
            region=storage_info['primary']['region'],
            unit_of_storage=storage_info['primary']['unit_of_storage']  # Include unit of storage in the query
        ).first()

        # If not found, try the secondary option
        if not storage_instance:
            storage_instance = StorageSpecifications.objects.filter(
                name=storage_info['secondary']['name'],
                sku=storage_info['secondary']['sku'],
                region=storage_info['secondary']['region'],
                unit_of_storage=storage_info['secondary']['unit_of_storage']  # Include unit of storage in the query
            ).first()

        if storage_instance:
            # Calculate the base unit price
            unit_price = float(storage_instance.unit_price)

            # Interpret unit of storage to calculate monthly price
            unit_of_storage = storage_instance.unit_of_storage.lower()
            # Define a set of keywords to identify different forms of unit storage
            gb_keywords = ['gb', 'gib/month', 'gb/month', '1/month']

            if any(keyword in unit_of_storage for keyword in gb_keywords):
                base_price = unit_price  # Convert to GB for consistency
            elif '10k/month' in unit_of_storage or '10k' in unit_of_storage:
                # Assuming '10k' means 10,000 KB and calculating for 1 TB
                kb_in_tb = 1024 * 1024 * 1024  # Total KB in 1 TB
                blocks_in_1TB = kb_in_tb / 10000  # Number of 10K blocks in 1 TB
                base_price = unit_price * blocks_in_1TB  # Adjust unit price to total price for 1 TB


            # Apply size multiplier based on storage size selected by user
            size_multiplier = size_multiplier_mapping_storage.get(storage_size, 1)
            price_monthly = base_price * size_multiplier
            storage_pice = float(price_monthly)

            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': f'{price_monthly:.2f}',  # Per unit price
                'price_monthly': f'{price_monthly:.2f}',  # Total monthly price based on size
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type,
                'unit_of_storage': storage_instance.unit_of_storage,
                'created_at': storage_instance.created_at.isoformat() if storage_instance.created_at else None,
            }
        else:
            computed_data['storage'] = 'No matching storage found'


        # Define networking type to name, SKU, unit of storage, and region mapping
    networking_to_name_and_sku_mapping = {
        'CDN': {
            'primary': {'name': 'Azure CDN from Microsoft - ', 'sku': 'WAF', 'unit_of_measure': '1M/Month'},
            'secondary': {'name': 'Azure CDN from Microsoft - ', 'sku': 'WAF', 'unit_of_measure': '1M/Month'}
        },
        'DNS': {
            'primary': {'name': 'Azure DNS - ', 'sku': 'Private', 'unit_of_measure': '1M'},
            'secondary': {'name': 'Azure DNS - ', 'sku': 'Public', 'unit_of_measure': '1M'}
        },
        # Add more mappings as necessary for different networking types
    }

        # Fetch DNS information if DNS connection is enabled
    if dns_connection == 'Yes':
        dns_info = networking_to_name_and_sku_mapping.get('DNS')
        if dns_info:
            dns_instance = NetworkingSpecifications.objects.filter(
                name=dns_info['primary']['name'],
                sku=dns_info['primary']['sku'],
                unit_of_measure=dns_info['primary']['unit_of_measure'],
            ).first() or NetworkingSpecifications.objects.filter(
                name=dns_info['secondary']['name'],
                sku=dns_info['secondary']['sku'],
                unit_of_measure=dns_info['secondary']['unit_of_measure'],
            ).first()

            if dns_instance:
                dns_price = float(dns_instance.unit_price)
                computed_data['networking'] = {
                    'name': dns_instance.name,
                    'unit_price': f'{float(dns_instance.unit_price):.2f} | Per 1,000,000 queries',
                    'sku': dns_instance.sku,
                    'provider': dns_instance.provider.name,
                    'cloud_service': dns_instance.cloud_service.service_type,
                    'unit_of_measure': dns_instance.unit_of_measure,
                    'created_at': dns_instance.created_at.isoformat() if dns_instance.created_at else None,
                }

    # Fetch CDN information if CDN connection is enabled
    if cdn_connection == 'Yes':
        cdn_info = networking_to_name_and_sku_mapping.get('CDN')
        if cdn_info:
            cdn_instance = NetworkingSpecifications.objects.filter(
                name=cdn_info['primary']['name'],
                sku=cdn_info['primary']['sku'],
                unit_of_measure=cdn_info['primary']['unit_of_measure'],
            ).first() or NetworkingSpecifications.objects.filter(
                name=cdn_info['secondary']['name'],
                sku=cdn_info['secondary']['sku'],
                unit_of_measure=cdn_info['secondary']['unit_of_measure'],
            ).first()

            if cdn_instance:
                cdn_price = float(cdn_instance.unit_price)
                # If computed_data['networking'] already has DNS data, append CDN data
                if 'networking' in computed_data:
                    combined_unit_price = float(computed_data['networking']['unit_price'].split('|')[0]) + float(cdn_instance.unit_price)
                    computed_data['networking'] = {
                        'name': f"{computed_data['networking']['name']}  {cdn_instance.name}",
                        'unit_price': f"{combined_unit_price:.2f} | Per 1,000,000 queries",
                        'sku': f"{computed_data['networking']['sku']} & {cdn_instance.sku}",
                        'provider': f"{computed_data['networking']['provider']} & {cdn_instance.provider.name}",
                        'cloud_service': f"{computed_data['networking']['cloud_service']} & {cdn_instance.cloud_service.service_type}",
                        'unit_of_measure': f"{computed_data['networking']['unit_of_measure']} & {cdn_instance.unit_of_measure}",
                        'created_at': cdn_instance.created_at.isoformat() if cdn_instance.created_at else None,
                    }
                else:
                    computed_data['networking'] = {
                        'name': cdn_instance.name,
                        'unit_price': f'{float(cdn_instance.unit_price):.2f} | Per 1,000,000 queries',
                        'sku': cdn_instance.sku,
                        'provider': cdn_instance.provider.name,
                        'cloud_service': cdn_instance.cloud_service.service_type,
                        'unit_of_measure': cdn_instance.unit_of_measure,
                        'created_at': cdn_instance.created_at.isoformat() if cdn_instance.created_at else None,
                    }


        # Calculating total monthly and annual prices
    monthly = compute_price + storage_pice + database_price + dns_price + cdn_price
    annual = monthly * 12

    # Adding monthly and annual totals to the computed_data dictionary
    computed_data['monthly'] = f'{monthly:.2f}'
    computed_data['annual'] = f'{annual:.2f}'

    return computed_data


def calculated_data_Azure_basic(compute_complexity, expected_users, data_storage_type, database_service, dns_feature, cdn_networking, region, budget):
    computed_data = {'provider': 'Microsoft Azure',}  # Initialize dictionary to store computed data
    compute_price = 0.0;
    storage_pice = 0.0;
    database_price = 0.0;
    dns_price = 0.0
    cdn_price = 0.0
    monthly = 0.0;
    annual = 0.0;

    # Mapping of user-friendly RAM/CPU options to SKU
    ram_to_sku_mapping = {
        'simple': 'Standard_F2',  # Example mapping, adjust based on actual data
        'moderate': 'Standard_D8ps_v5',  # Example mapping
        'complex': 'Standard_B16as_v2',  # Example mapping
        # add mappings as necessary
    }

    # Retrieve the SKU from the mapping based on the expected_ram
    expected_sku = ram_to_sku_mapping.get(compute_complexity)

        # Retrieve data from the database based on the provided SKU
    if expected_sku:
        compute_instance = ComputeSpecifications.objects.filter(sku=expected_sku).first()
        if compute_instance:
            # Base instance name with location
            instance_name = f"{compute_instance.name} [US East (N. Virginia)]"

            compute_price = float(compute_instance.price_monthly)

            computed_data['compute'] = {
                'name': instance_name,
                'unit_price': compute_instance.price_monthly,
                'cpu': compute_instance.cpu,
                'memory': compute_instance.memory,
                'sku': compute_instance.sku,
                'provider': compute_instance.provider.name,
                'cloud_service': compute_instance.cloud_service.service_type,
                'price_monthly': compute_instance.price_monthly,
                'created_at': compute_instance.created_at.isoformat() if compute_instance.created_at else None,
            }


    # Assuming these are price multipliers for different service tiers or capacities
    size_multiplier_mapping = {
        '1000': 10,    # 50 GB
        '5000': 100,  # 200 GB
        '10000': 1000,  # 1000 T
    }

    service_to_name_and_sku_mapping = {
        'basic': {
            'primary': {
                'name': 'Azure Cosmos DB',
                'sku': 'RUm',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            },
            'secondary': {
                'name': 'Azure Cosmos DB for MongoDB vCore',
                'sku': 'General Purpose Storage',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            }
        },
        'complex': {
            'primary': {
                'name': 'SQL Database Standard - Storage',
                'sku': 'Standard',
                'region': 'East US',
                'unit_of_storage': '1 GB/Month'
            },
            'secondary': {
                'name': 'SQL Database Premium - Storage',
                'sku': 'Premium',
                'region': 'eastus',
                'unit_of_storage': '1 GB/Month'
            }
        },
        'nodatabase': {
            'primary': {
                'name': '',
                'sku': '',
                'region': '',
                'unit_of_storage': ''
            },
            'secondary': {
                'name': '',
                'sku': '',
                'region': '',
                'unit_of_storage': ''
            }
        }
    }

    service_info = service_to_name_and_sku_mapping.get(database_service)

    if service_info:
        database_instance = DatabaseSpecifications.objects.filter(
            name=service_info['primary']['name'],
            sku=service_info['primary']['sku'],
            region=service_info['primary']['region'],
            unit_of_storage=service_info['primary']['unit_of_storage']
        ).first()

        if not database_instance:
            database_instance = DatabaseSpecifications.objects.filter(
                name=service_info['secondary']['name'],
                sku=service_info['secondary']['sku'],
                region=service_info['secondary']['region'],
                unit_of_storage=service_info['secondary']['unit_of_storage']
            ).first()

        if database_instance:
            size_multiplier = size_multiplier_mapping.get(expected_users, 1)
            unit_price = float(database_instance.unit_price)  # Assume this gives price per GB/Month
            # Calculate the price for the selected size
            total_price = unit_price * size_multiplier  # Assuming price needs to be calculated per TB
            database_price = float(total_price)

            computed_data['database'] = {
                'name': database_instance.name,
                'unit_price': f'{total_price:.2f}',
                'total_price': f'{total_price:.2f}',
                'sku': database_instance.sku,
                'region': database_instance.region,
                'unit_of_storage': database_instance.unit_of_storage,
                'data_type': database_instance.data_type,
                'provider': database_instance.provider.name,
                'cloud_service': database_instance.cloud_service.service_type,
                'created_at': database_instance.created_at.isoformat() if database_instance.created_at else None,
            }
        else:
            computed_data['database'] = 'No matching database found'
    else:
        computed_data['database'] = 'Service not found'


    # Define size to price multiplier mapping, adjust as needed
    size_multiplier_mapping_storage = {
        '1000': 10,    # 50 GB
        '5000': 100,  # 200 GB
        '10000': 1000,  # 1000 T
    }

        # Define storage type to name, SKU, region, and unit of storage mapping with primary and secondary options
    storage_to_name_and_sku_mapping_storage = {
        'multimedia': {
            'primary': {'name': 'General Block Blob', 'sku': 'Standard GRS', 'region': 'uksouth', 'unit_of_storage': '1 GB/Month'},
            'secondary': {'name': 'General Block Blob v2', 'sku': 'Cold RA-GZRS', 'region': 'uksouth', 'unit_of_storage': '1 GB'}
        },
        'files': {
            'primary': {'name': 'Files', 'sku': 'Standard LRS', 'region': 'brazilsoutheast', 'unit_of_storage': '1 GB/Month'},
            'secondary': {'name': 'Files v2', 'sku': 'Cool GRS', 'region': 'westeurope', 'unit_of_storage': '1 GB'}
        },
        'databases': {
            'primary': {'name': 'Standard SSD Managed Disks', 'sku': 'E3 LRS', 'region': 'attnewyork1', 'unit_of_storage': '1/Month'},
            'secondary': {'name': 'Standard SSD Managed Disks', 'sku': 'E3 LRS', 'region': 'norwaywest', 'unit_of_storage': '1/Month'}
        },
        'No Storage': {
            'primary': {'name': '', 'sku': '', 'region': '', 'unit_of_storage': ''},
            'secondary': {'name': '', 'sku': '', 'region': '', 'unit_of_storage': ''}  # Adjust as needed
        }
        # Add more mappings as necessary for different storage types
    }

    storage_info = storage_to_name_and_sku_mapping_storage.get(data_storage_type)

    if storage_info:
        # Attempt to fetch the primary storage instance
        storage_instance = StorageSpecifications.objects.filter(
            name=storage_info['primary']['name'],
            sku=storage_info['primary']['sku'],
            region=storage_info['primary']['region'],
            unit_of_storage=storage_info['primary']['unit_of_storage']  # Include unit of storage in the query
        ).first()

        # If not found, try the secondary option
        if not storage_instance:
            storage_instance = StorageSpecifications.objects.filter(
                name=storage_info['secondary']['name'],
                sku=storage_info['secondary']['sku'],
                region=storage_info['secondary']['region'],
                unit_of_storage=storage_info['secondary']['unit_of_storage']  # Include unit of storage in the query
            ).first()

        if storage_instance:
            # Calculate the base unit price
            unit_price = float(storage_instance.unit_price)

            # Interpret unit of storage to calculate monthly price
            unit_of_storage = storage_instance.unit_of_storage.lower()
            # Define a set of keywords to identify different forms of unit storage
            gb_keywords = ['gb', 'gib/month', 'gb/month', '1/month']

            if any(keyword in unit_of_storage for keyword in gb_keywords):
                base_price = unit_price  # Convert to GB for consistency
            elif '10k/month' in unit_of_storage or '10k' in unit_of_storage:
                # Assuming '10k' means 10,000 KB and calculating for 1 TB
                kb_in_tb = 1024 * 1024 * 1024  # Total KB in 1 TB
                blocks_in_1TB = kb_in_tb / 10000  # Number of 10K blocks in 1 TB
                base_price = unit_price * blocks_in_1TB  # Adjust unit price to total price for 1 TB


            # Apply size multiplier based on storage size selected by user
            size_multiplier = size_multiplier_mapping_storage.get(expected_users, 1)
            price_monthly = base_price * size_multiplier
            storage_pice = float(price_monthly)

            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': f'{price_monthly:.2f}',  # Per unit price
                'price_monthly': f'{price_monthly:.2f}',  # Total monthly price based on size
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type,
                'unit_of_storage': storage_instance.unit_of_storage,
                'created_at': storage_instance.created_at.isoformat() if storage_instance.created_at else None,
            }
        else:
            computed_data['storage'] = 'No matching storage found'


        # Define networking type to name, SKU, unit of storage, and region mapping
    networking_to_name_and_sku_mapping = {
        'CDN': {
            'primary': {'name': 'Azure CDN from Microsoft - ', 'sku': 'WAF', 'unit_of_measure': '1M/Month'},
            'secondary': {'name': 'Azure CDN from Microsoft - ', 'sku': 'WAF', 'unit_of_measure': '1M/Month'}
        },
        'DNS': {
            'primary': {'name': 'Azure DNS - ', 'sku': 'Private', 'unit_of_measure': '1M'},
            'secondary': {'name': 'Azure DNS - ', 'sku': 'Public', 'unit_of_measure': '1M'}
        },
        # Add more mappings as necessary for different networking types
    }

        # Fetch DNS information if DNS connection is enabled
    if dns_feature == 'Yes':
        dns_info = networking_to_name_and_sku_mapping.get('DNS')
        if dns_info:
            dns_instance = NetworkingSpecifications.objects.filter(
                name=dns_info['primary']['name'],
                sku=dns_info['primary']['sku'],
                unit_of_measure=dns_info['primary']['unit_of_measure'],
            ).first() or NetworkingSpecifications.objects.filter(
                name=dns_info['secondary']['name'],
                sku=dns_info['secondary']['sku'],
                unit_of_measure=dns_info['secondary']['unit_of_measure'],
            ).first()

            if dns_instance:
                dns_price = float(dns_instance.unit_price)
                computed_data['networking'] = {
                    'name': dns_instance.name,
                    'unit_price': f'{float(dns_instance.unit_price):.2f} | Per 1,000,000 queries',
                    'sku': dns_instance.sku,
                    'provider': dns_instance.provider.name,
                    'cloud_service': dns_instance.cloud_service.service_type,
                    'unit_of_measure': dns_instance.unit_of_measure,
                    'created_at': dns_instance.created_at.isoformat() if dns_instance.created_at else None,
                }

    # Fetch CDN information if CDN connection is enabled
    if cdn_networking == 'Yes':
        cdn_info = networking_to_name_and_sku_mapping.get('CDN')
        if cdn_info:
            cdn_instance = NetworkingSpecifications.objects.filter(
                name=cdn_info['primary']['name'],
                sku=cdn_info['primary']['sku'],
                unit_of_measure=cdn_info['primary']['unit_of_measure'],
            ).first() or NetworkingSpecifications.objects.filter(
                name=cdn_info['secondary']['name'],
                sku=cdn_info['secondary']['sku'],
                unit_of_measure=cdn_info['secondary']['unit_of_measure'],
            ).first()

            if cdn_instance:
                cdn_price = float(cdn_instance.unit_price)
                # If computed_data['networking'] already has DNS data, append CDN data
                if 'networking' in computed_data:
                    combined_unit_price = float(computed_data['networking']['unit_price'].split('|')[0]) + float(cdn_instance.unit_price)
                    computed_data['networking'] = {
                        'name': f"{computed_data['networking']['name']}  {cdn_instance.name}",
                        'unit_price': f"{combined_unit_price:.2f} | Per 1,000,000 queries",
                        'sku': f"{computed_data['networking']['sku']} & {cdn_instance.sku}",
                        'provider': f"{computed_data['networking']['provider']} & {cdn_instance.provider.name}",
                        'cloud_service': f"{computed_data['networking']['cloud_service']} & {cdn_instance.cloud_service.service_type}",
                        'unit_of_measure': f"{computed_data['networking']['unit_of_measure']} & {cdn_instance.unit_of_measure}",
                        'created_at': cdn_instance.created_at.isoformat() if cdn_instance.created_at else None,

                    }
                else:
                    computed_data['networking'] = {
                        'name': cdn_instance.name,
                        'unit_price': f'{float(cdn_instance.unit_price):.2f} | Per 1,000,000 queries',
                        'sku': cdn_instance.sku,
                        'provider': cdn_instance.provider.name,
                        'cloud_service': cdn_instance.cloud_service.service_type,
                        'unit_of_measure': cdn_instance.unit_of_measure,
                        'created_at': cdn_instance.created_at.isoformat() if cdn_instance.created_at else None,
                    }


        # Calculating total monthly and annual prices
    monthly = compute_price + storage_pice + database_price + dns_price + cdn_price
    annual = monthly * 12

    # Adding monthly and annual totals to the computed_data dictionary
    computed_data['monthly'] = f'{monthly:.2f}'
    computed_data['annual'] = f'{annual:.2f}'

    return computed_data