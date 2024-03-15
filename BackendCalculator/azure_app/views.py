from rest_framework import viewsets
import requests
from rest_framework.response import Response
from django.http import HttpResponse
from databaseServer.models import Provider, CloudService, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications, ComputeSpecifications

class ViewHello(viewsets.ViewSet):

    # Define a custom action named 'hello'
    def list(self, request):
        return Response("hello")

# Azure compute fetch
def compute_fetch_view(request):
    return HttpResponse("Data fetched and stored successfully")


# Azure storage fetch
def storage_fetch_view(request):
     # Clear existing storage data from the database
    StorageSpecifications.objects.all().delete()
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
    # Clear existing networking data from the database
    NetworkingSpecifications.objects.all().delete()

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

            NetworkingSpecifications.objects.create(
                name=service.get('productName', 'N/A'),
                provider=provider,
                cloud_service=cloud_service,
                sku=service.get('skuName', 'N/A'),
                unit_price=service.get('retailPrice', '0.0'),
                unit_of_measure=service.get('unitOfMeasure', 'N/A'),
                region=service.get('armRegionName', 'No region provided')
            )

    # Fetch pricing data for networking services
    service_names = ["Content Delivery Network", "Virtual Network"]  # Update with desired service names
    for service_name in service_names:
        print(f"Fetching pricing data for: {service_name}")
        pricing_data = fetch_azure_pricing(service_name)
        store_pricing_data(pricing_data)

    return HttpResponse("Networking pricing data fetched and stored successfully.")


# Azure database fetch
def database_fetch_view(request):
    # Clear existing database data from the database
    DatabaseSpecifications.objects.all().delete()

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



# the backend logic for advanced form
def calculated_data_Azure(database_service, expected_cpu, cloud_storage, networking_feature):
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

# the backend logic for advanced form
def calculated_data_Oracle(database_service, expected_cpu, cloud_storage, networking_feature):
    computed_data = {'provider': 'Oracle',}  # Initialize dictionary to store computed data

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