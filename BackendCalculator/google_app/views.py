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
service_filter = "service=\"services/9662-B51E-5089\"" #cloud sql
service_filter_storage="service=\"services/95FF-2EF5-5EA1\"" #cloud storage
desired_categories = ['MySQL', 'Postgres', 'SQL Server']
output_file_path = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/specs_info.json'
output_file_path2 = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/price_info.json'
storage_combined = "C:/Users/Joseph/Documents/storageprice.json"
output_file_Storage="C:/Users/Joseph/Documents/storageinfo.json"
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
    #Getting storage specs
    #get_storage_specs(endpoint_url,API_KEY,service_filter_storage,output_file_Storage)
    #getting prices and inserting into db--
    #retrieve_prices_from_json(output_file_Storage,API_KEY,storage_combined)
    
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
        # Iterate over cost details for each region
        for region, region_details in instance_details['cost'].items():
            # Populate the fields for each region
            compute_spec = ComputeSpecifications()
            compute_spec.name = instance
            compute_spec.provider=provider
            compute_spec.cloud_service=cloud_service
            compute_spec.sku = str(uuid.uuid4())
            compute_spec.cpu = instance_details['cpu']
            compute_spec.memory = instance_details['ram']
            compute_spec.region = region
            compute_spec.unit_price = region_details['hour']  #Change this to month to avoid calculation at the end
            
            # Save the ComputeSpecifications object
            compute_spec.save()
    
    print("Compute information stored successfully")
    
    
def get_storage_specs(endpoint_url, api_key, service_filter, output_file_path):
    all_skus = []
    next_page_token = None

    while True:
        # Construct the request URL with parameters including the next page token if available
        request_url = f"{endpoint_url}?key={api_key}&pageSize=5000&filter={service_filter}"
        if next_page_token:
            request_url += f"&pageToken={next_page_token}"

        # Send GET request to the API endpoint
        response = requests.get(request_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract information from the response and filter based on category
            skus = data.get('skus', [])
            filtered_skus = [sku for sku in skus if any(category.get('category') in ['Nearline', 'Coldline', 'Archive', 'Standard'] for category in sku.get('productTaxonomy', {}).get('taxonomyCategories', []))]
            all_skus.extend(filtered_skus)

            # Check if there is a next page token
            next_page_token = data.get('nextPageToken')

            # Break the loop if there is no next page token
            if not next_page_token:
                break
        else:
            print(f"Error: {response.status_code} - {response.reason}")

    # Save the formatted response to a JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(all_skus, json_file, indent=2)
            
# for each sku id found in the file it will call the api to get the details for that skuid (price) and write to file, This functon gets called by the other function below
def get_google_cloud_sku_prices(sku_id, api_key, page_size=5000, page_token=None):
    url = f"https://cloudbilling.googleapis.com/v1beta/skus/{sku_id}/prices?key={api_key}&pageSize={page_size}"
    if page_token:
        url += f"&pageToken={page_token}"

    response = requests.get(url)
    data = response.json()

    return data

#goes through each one of the skuid in the file and then sends that skuid to the function above to get price

def retrieve_prices_from_json(json_file, api_key, output_file):
    with open(json_file) as f:
        skus_data = json.load(f)

    combined_data = {}
    for sku_info in skus_data:
        sku_id = sku_info['skuId']
        prices_data = get_google_cloud_sku_prices(sku_id, api_key)
        combined_data[sku_id] = {
            'sku_info': sku_info,
            'prices_data': prices_data
        }
        with open(output_file, 'w') as outfile:
            json.dump(combined_data, outfile, indent=2)

print(f'All SKUs saved to {output_file_path}')      
    

#THE CODE BELOW IS LOGIC 


# def calculated_data_gcp(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
#     # Query Compute Specifications based on expected CPU and location
#     compute_services = ComputeSpecifications.objects.filter(provider__name='GCP', cpu__gte=expected_cpu, region=location)

#     totalprice=0.0
#     for compute_service in compute_services:
#         total_price += float(compute_service.unit_price)
        
#     gcp_data = {
#         "compute_services" : list(compute_services.values())
#     }
#     return gcp_data

def calculated_data_gcp(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    
    computed_data = {'provider': 'Google Cloud',}  # Initialize dictionary to store computed data
    # Retrieve data from the database based on the provided keyword
    compute_name=None
    if expected_cpu == "1vCPUs":
        compute_name="n1-standard-1"
    elif expected_cpu == "2vCPUs":
        compute_name="n1-standard-2"
    elif expected_cpu == "4vCPUs":
        compute_name="n1-standard-4"
    elif expected_cpu == "8vCPUs":
        compute_name="n2-standard-8"
    elif expected_cpu == "12vCPUs":
        compute_name="g2-standard-12"
    elif expected_cpu == "16vCPUs":
        compute_name="n1-standard-16"
        # Query for the first compute instance
        
        # the instance type and region
    compute_instance = ComputeSpecifications.objects.filter(provider__name='GCP', name=compute_name, region=location).first()
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
        storage_instance = StorageSpecifications.objects.filter(name__icontains="")
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
            
    # #Database Logic
    db_type=None
    if database_service== 'postgreSQL':
        db_type= "PostgreSQL"
    elif database_service == 'sql':
        db_type= "SQL Server"
    elif database_service == 'NoSql':
        db_type= "NoSQL"
    
    #Going through the region to set the location for query
    city=None
    if location == "us-central1":
        city= "Iowa"
    elif location == "us-east1":
        city= "South Carolina"
    elif location == "us-east4":
        city="Northern Virginia"
    elif location == "us-east5":
        city= "Columbus"
    elif location == "us-south1":
        city= "Dallas"
    elif location == "us-west1":
        city= "Oregon"
    elif location == 'us-west2':
        city= "Los Angeles"
    elif location == "us-west3":
        city="Salt Lake City"
    elif location == "us-west4":
        city= "Las Vegas"
    elif location == "asia-east2":
        city="Hong Kong"
    elif location == "asia-east1":
        city="Taiwan"
    elif location == "asia-northeast1":
        city= "Tokyo"
    elif location == "asia-northeast2":
        city= "Osaka"
    elif location == "asia-northeast3":
        city= "Seoul"
    elif location == "asia-south1":
        city= "Mumbai"
    elif location == "asia-south2":
        city= "Delhi"
    elif location == "asia-southeast1":
        city= "Singapore"
    elif location == "asia-southeast2":
        city= "Jakarta"
    elif location == "australia-southeast1":
        city= "Sydney"
    elif location == "australia-southeast2":
        city= "Melbourne"
    elif location == "europe-central2":
        city= "Warsaw"
    elif location == "europe-north1":
        city= "Finland"
    elif location == "europe-southwest1":
        city= "Madrid"
    elif location == "europe-west1":
        city= "Belgium"
    elif location == "europe-west2":
        city= "London"
    elif location == "europe-west3":
        city= "Frankfurt"
    elif location == "europe-west4":
        city= "Netherlands"
    elif location == "europe-west6":
        city= "Zurich"
    elif location == "europe-west8":
        city= "Milan"
    elif location == "europe-west9":
        city= "Paris"
    elif location == "me-west1":
        city= "Tel Aviv"
    elif location == "northamerica-northeast1":
        city= "Montréal"
    elif location == "northamerica-northeast2":
        city= "Toronto"
    elif location == "southamerica-east1":
        city= "São Paulo"
    elif location == "southamerica-west1":
        city= "Santiago"
    # db_type="PostgreSQL"
    # city="Dallas"
    if db_type and city:
        query_template = "Cloud SQL for %s: Regional - Standard storage in %s"
        query= query_template % (db_type, city)
        # Query for the first database instance
        database_instance = DatabaseSpecifications.objects.filter(name=query).first()
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
    #     else:
    #         computed_data['networking']= None

    return computed_data

def callmain(request):
    main()
    return HttpResponse("Main function called successfully.")

if __name__ == "__main__":
    main()

