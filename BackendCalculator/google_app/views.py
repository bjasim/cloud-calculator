import json
import yaml
import uuid
from databaseServer.models import DatabaseSpecifications, CloudService, Provider, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials  
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError  
import os.path
import requests
from django.http import HttpResponse

# Define the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/cloud-billing.readonly']
endpoint_url = "https://cloudbilling.googleapis.com/v2beta/skus"

API_KEY = "AIzaSyB6TLXAdnJCDoCBX_tPm8zU_PBA-jj7MG8"
service_filter = "service=\"services/9662-B51E-5089\""
desired_categories = ['MySQL', 'Postgres', 'SQL Server']
output_file_path = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/specs_info.json'
output_file_path2 = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/price_info.json'
combined_info= 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/combined_info.json'


def main():
    # Get authenticated service
    service = get_authenticated_service()
    # Get SKUs for a specific service
    service_name = "services/9662-B51E-5089"  # CloudSQL service name
    #Getting the price for all skus with above parent service
    #get_prices(service,service_name)
    #Getting all parent service sku information (getting specifications about each sku)
    #get_specs(endpoint_url, API_KEY, service_filter, desired_categories, output_file_path)
    #compute info
    computeinfo()
    # Create a new function to combine the information from the two json files based on skuid and insert into the db
    #combine_json_data(output_file_path, output_file_path2,combined_info)
    #write to DB 
    
def get_authenticated_service():
    # Check if credentials file exists
    creds = None
    if os.path.exists('token.json'):
        # Load credentials from file if it exists
        creds = Credentials.from_authorized_user_file('token.json')
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/Joseph/Downloads/client_secrets_file-1.json',  # Replace with your client secrets file path
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service using the authenticated credentials
    service = build('cloudbilling', 'v1', credentials=creds)
    return service
    
    
def get_prices(service, service_name):
    try:
        next_page_token = None
        filtered_info = []

        while True:
            request = service.services().skus().list(parent=service_name, pageToken=next_page_token)
            response = request.execute()
            skus = response.get('skus', [])
            next_page_token = response.get('nextPageToken', None)

            print(f'\nSKUs for {service_name}:')
            for sku in skus:
                print(f"Name: {sku['name']}")
                print(f"Description: {sku['description']}")
                print(f"Category: {sku['category']['resourceFamily']} - {sku['category']['resourceGroup']}")
                print(f"Pricing info: {sku['pricingInfo']}")
                print()

                filtered_info.append({
                    'name': sku['name'],
                    'description': sku['description'],
                    'category': {
                        'resourceFamily': sku['category']['resourceFamily'],
                        'resourceGroup': sku['category']['resourceGroup'], 
                    },
                    'pricingInfo': sku['pricingInfo']
                })

            if not next_page_token:
                break

        with open(output_file_path2, 'w') as json_file:
            json.dump(filtered_info, json_file, indent=2)

        print(f'Filtered information saved to {output_file_path2}')

    except HttpError as e:
        print(f"HttpError: {e}")
        print(f"Response content: {e.content}")
        print(f"Response status: {e.resp.status}")
        print(f"Response reason: {e.resp.reason}")
        print(f"Response details: {e._get_reason()}")
        print(f"URI: {e.uri}")
        print(f"Error details: {e.error_details}")
def get_specs(endpoint_url, API_KEY, service_filter, desired_categories, output_file_path):
    # Initialize an empty list to store all SKUs
    all_skus = []

    # Initialize the next page token
    next_page_token = None

    while True:
        # Construct the request URL with parameters including the next page token if available
        request_url = f"{endpoint_url}?key={API_KEY}&pageSize=5000&filter={service_filter}"
        if next_page_token:
            request_url += f"&pageToken={next_page_token}"

        # Send GET request to the API endpoint
        response = requests.get(request_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract information from the response
            skus = data.get('skus', [])
            all_skus.extend(skus)

            # Check if there is a next page token
            next_page_token = data.get('nextPageToken')

            # Break the loop if there is no next page token
            if not next_page_token:
                break
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return

    # Reformatting response as requested
    filtered_skus = [sku for sku in all_skus if any(desired_category in [category['category'] for category in sku['productTaxonomy']['taxonomyCategories']] for desired_category in desired_categories)]

    # Print the formatted response
    print(json.dumps(filtered_skus, indent=2))

    # Save the formatted response to a JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(filtered_skus, json_file, indent=2)

    print(f'Formatted response saved to {output_file_path}')

def combine_json_data(file1_path, file2_path, output_file_path):
    provider_name = 'GCP'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Database'  # Assuming 'Database' is the service_type for database-related services
    cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type=cloud_service_type)
    
    
    # Load the content of the first JSON file
    with open(file1_path, 'r') as spec_file:
        spec_info = json.load(spec_file)

    # Load price_info.json
    with open(file2_path, 'r') as price_file:
        price_info = json.load(price_file)

    # Iterate over spec_info to find matching skuIds in price_info
    
    combined_data = {}
    combined_data['skus'] = []
    
    for specs_sku in spec_info:
        sku_id = specs_sku['skuId']
        for price_sku in price_info:
            if sku_id in price_sku['name']:
                combined_sku = {
                    'skuId': specs_sku['skuId'],
                    'displayName': specs_sku['displayName'],
                    'category': price_sku['category'],
                    'pricingInfo': price_sku['pricingInfo'],
                    'productTaxonomy': specs_sku['productTaxonomy'],
                    'geoTaxonomy': specs_sku['geoTaxonomy']
                }
                combined_data['skus'].append(combined_sku)
                break
    
    with open(output_file_path, 'w') as combined_f:
        json.dump(combined_data, combined_f, indent=2)
    
        
    with open(output_file_path, 'r') as file:
        combined_data = json.load(file)

    for sku_entry in combined_data['skus']:
        # Extract relevant data from the JSON
        sku_id = sku_entry['skuId']
        display_name = sku_entry['displayName']
        category = sku_entry['productTaxonomy']['taxonomyCategories']
        #region = sku_entry['geoTaxonomy']['regionalMetadata']['region']['region']

        # Extract database type from category
        data_type = None
        for cat in category:
            if 'MySQL' in cat['category']:
                data_type = 'MySQL'
            elif 'Postgre' in cat['category']:
                data_type = 'PostgreSQL'
            elif 'SQL Server' in cat['category']:
                data_type = 'SQL Server'
                 
        pricing_info = sku_entry.get('pricingInfo', [{}])[0]  # Assuming only one pricing info entry
        tiered_rates = pricing_info.get('pricingExpression', {}).get('tieredRates', [])
        unit_price = tiered_rates[0].get('unitPrice', {}).get('units', 'Unknown')
        price_nanos = tiered_rates[0].get('unitPrice', {}).get('nanos', 'Unknown')

        
        region_data = sku_entry.get('geoTaxonomy', {}).get('regionalMetadata', {})
        region = region_data.get('region', {}).get('region', 'No region provided')
        

        # Create DatabaseSpecifications object and save it
        if data_type:
            DatabaseSpecifications.objects.create(
                name=display_name,
                provider=provider,
                cloud_service=cloud_service,
                data_type=data_type,
                sku=sku_id,
                unit_price=price_nanos,  
                unit_of_storage=unit_price,              
                region=region              
            )
                    
def computeinfo():
    url = 'https://github.com/Cyclenerd/google-cloud-pricing-cost-calculator/raw/master/pricing.yml'
    destination_file = 'google_app/pricing.yml'
    response = requests.get(url)
    provider_name = 'GCP'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Compute'  # Assuming 'Database' is the service_type for database-related services
    cloud_service, _ = CloudService.objects.get_or_create(provider=provider, service_type=cloud_service_type)

    if response.status_code == 200:
        with open(destination_file, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully as '{destination_file}'")
    else:
        print("Failed to download the file.")
        
    with open(destination_file, 'r') as file:
        data = yaml.safe_load(file)

    # Assuming 'compute' is the key in your YAML file
    compute_data = data['compute']

    
    # Iterate over instance data
    for instance, instance_details in compute_data['instance'].items():
        # Create a new ComputeSpecifications object for each instance
        compute_spec = ComputeSpecifications()
        compute_spec.name = instance
        compute_spec.provider=provider
        compute_spec.cloud_service=cloud_service
        compute_spec.sku = str(uuid.uuid4())
        compute_spec.cpu = instance_details['cpu']
        compute_spec.memory = instance_details['ram']
        
        # Iterate over cost details for each region
        for region, region_details in instance_details['cost'].items():
            # Populate the fields for each region
            compute_spec.region = region
            compute_spec.unit_price = region_details['hour']
            
            # Save the ComputeSpecifications object
            compute_spec.save()
    
    print("Compute information stored successfully")
    
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
        else:
            computed_data['storage']= None

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
        else:
            computed_data['networking']= None

    return computed_data

def callmain(request):
    main()
    return HttpResponse("Main function called successfully.")

if __name__ == "__main__":
    main()

