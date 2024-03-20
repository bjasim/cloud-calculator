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
endpoint_url2 ="https://cloudbilling.googleapis.com/v1/services/9662-B51E-5089/skus"

API_KEY = "AIzaSyB6TLXAdnJCDoCBX_tPm8zU_PBA-jj7MG8"

#DATABASE
service_filter = "service=\"services/9662-B51E-5089\"" #cloud sql service
desired_categories = ['MySQL', 'Postgres', 'SQL Server']
output_file_path = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/specs_info.json'
output_file_path2 = 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/price_info.json'
combined_info= 'C:/Users/Joseph/cloud-calculator/cloud-calculator/BackendCalculator/google_app/combined_info.json'

#STORAGE 
service_filter_storage="service=\"services/95FF-2EF5-5EA1\"" #cloud storage
storage_combined = "C:/Users/Joseph/Documents/storageprice.json"
output_file_Storage="C:/Users/Joseph/Documents/storageinfo.json"

# Skus for all relevant  services, the following array includes Skus for Cloud CDN and Cloud DNS
loadbalacer_skus = [
    '0427-AC0E-DEAF', '074C-3176-B6B1', '0805-38B4-A6AA',
    '0BE3-FB0A-41B5', '130D-D8B9-8C01', '1448-AE6A-3DFD',
    '1497-0D02-1D98', '1538-E533-F41F', '1603-E19B-DD92',
    '1752-6065-3660', '1B1F-B284-2AF9', '22EA-A3F3-D43E',
    '2A55-54D9-70F4', '2C71-0AFA-E05A', '2D99-1312-BBAB',
    '2DA4-60F8-167D', '3004-4CDD-0CFB', '3275-05B0-D475',
    '333D-F545-6705', '3546-A4D3-F710', '3A80-35DD-8213',
    '3F60-2E4F-0911', '454E-9A7D-F9D5', '46A6-3157-39E1',
    '4AD7-DE70-A9F7', '4CA1-8FD0-21EE', '5A74-0128-8187',
    '5D20-55B9-6896', '5EEB-601A-4B74', '62F2-9E12-5F44',
    '634A-3C77-A50A', '6447-DBD0-130A', '6461-9B80-88EB',
    '6692-4B3B-9E35', '7022-A7D6-7D82', '7087-03B4-CF6F',
    '732B-7574-0DDC', '77C0-9E0C-76B0', '7817-144B-A5AC',
    '7A0E-3D45-C93B', '7DE5-A1CE-27D7', '82A1-DB74-B3FA',
    '8365-2032-F1D3', '8562-97A0-797E', '8625-A380-1224',
    '8681-2E73-F5B0', '8868-408C-BF4B', '9139-E803-FACE',
    '949C-F222-A9F1', '9666-1DDE-5905', '9859-3C2C-5FE1',
    '9895-3D84-C97F', '9BB3-3C40-2809', '9DF3-2AC6-2D3E',
    'A0D5-35E8-DDE0', 'A200-33A3-245F', 'A60F-0E11-6E0C',
    'A650-E839-CDB6', 'A7BC-0A86-BB2E', 'AA4D-A91E-8D75',
    'AE3D-4662-FCEF', 'B140-DACF-3365', 'B212-B2EA-6B8D',
    'B338-7E43-8EBA', 'B380-B567-6D29', 'B468-6105-7883',
    'B955-5B44-BD28', 'B9BD-6489-535E', 'BC7E-076A-0571',
    'C136-EB77-2990', 'C2EB-B343-5192', 'C88B-3016-1C60',
    'D008-DADF-093C', 'D107-DA77-EE8C', 'D27A-42CE-1A3A',
    'D683-33F2-5C47', 'D727-6F37-F264', 'D83A-C047-F3B5',
    'DCE9-C1CA-81B2', 'E4FD-CE95-F940', 'EBCE-61F1-6CE7',
    'F051-558E-CBE7', 'F0C7-4A86-E056', 'F0DD-1D41-B68D',
    'F2A9-01F4-E934', '0CAB-FE26-F2C6'
]

block_storage_skus = ["0306-B164-A7B7","0572-568A-4FC4","17A8-D0A4-D7E5","1F1F-0EF5-15BE","23BD-C186-EF37","28D0-437A-CEAD","320C-7688-1A62","5334-92F9-3E7F","5881-96B1-93E3","5A6A-4A16-F865","7A7B-EA46-2897","7EA3-FF02-75C9","80E2-7FF9-979E","83E4-C062-FDEC","8AF1-1146-E7DA","92E5-B76E-D04B","95EE-349E-CA35","9917-39D5-DB38","9917-39D5-DB38","9977-2BC5-386A","9CB9-1019-8019","A084-03C1-A923","A9A2-174F-91A0","AE8C-46C3-4994","B287-C627-C943","B749-AAF2-5AC4","BF1A-6647-009D","BF8D-1C96-EE1C","CEF4-0773-7924","D279-B8D7-090F","D619-8E03-F681","DF49-E005-E705","E083-93C6-55CD","E45C-6460-E782","E763-1A59-7698","EEFE-F863-E07A","F993-B67E-E316","D973-5D65-BAB2"]
#F17B-412E-CB64 FOR APP ENGINE
firestore_skus = [
    "C005-5223-1DA2", "64CD-37E7-E98C", "BE4B-05D1-89E3", "D857-DB63-AF95",
    "57E7-37FE-8BE1", "4911-84A4-3BF8", "8B94-29E1-9E8C", "DEDB-38C1-A9E7",
    "82DB-114D-ADD9", "F8AE-9B57-B8AB", "081D-E9E6-8764", "7D87-7C62-0BDF",
    "725E-AC6D-1DF2", "BDE6-81DE-92B3", "D4E6-CE1B-6A45", "05C9-D9B3-A288",
    "50A0-CE13-FEFA", "0D19-F673-9BAE", "9CA4-6089-4B94", "B58E-B142-80A0",
    "03B5-5C26-0A59", "4B85-D08E-36CF", "944B-88B4-C839", "5805-1CBD-EED6",
    "987B-3E52-3AAD", "5A9C-0028-BEE2", "E80F-D346-F80E", "8A08-42E8-AC59",
    "C47E-F06B-15CF", "995E-226B-C6B2", "E270-723E-CFC6", "F318-B187-44F6",
    "712B-54D4-F3C9", "8979-BD7B-638C", "2793-76AA-56C9", "0D43-B821-BD27",
    "BCF3-E44E-0182", "8083-93BB-F13A", "802A-A763-295B","5C80-18C6-21C5"
]
filestore_skus= [
    "559A-0506-7B0A", "D149-0966-D3EA", "ABBD-1012-8CAB",
    "40C7-C133-48C1", "8789-2E1F-DD35", "C7B1-C2AB-8FB3",
    "F7F7-BABE-3C0D", "1675-34BD-A7AD", "1CF8-3D90-ED7A",
    "B315-A685-9DC4", "D0C4-A7AF-FCE8", "BD98-0C8E-B52B",
    "49F0-CDF0-8A41", "C4D4-3CC1-EA04", "FD2A-CA44-05B9",
    "9851-EB15-3A2F", "0CC7-15EB-7F77", "3DD1-7333-DD1E",
    "BA6C-7537-6045", "637E-F5F6-8B5E", "3B6C-72D5-47D5",
    "A6FF-1F2B-B99D", "A4FA-97A6-FE9D", "81AC-9287-2FA4",
    "28E9-AF7A-9107", "9ECF-18E5-1649", "EEB6-F2A3-670C",
    "E3C7-752B-C3EA", "4FFE-CED3-540C", "FC3D-DA69-44D4",
    "8424-E89C-4CBE", "47BC-DFD4-04CD", "24BB-417D-4E26",
    "88D6-264C-F61C", "6B47-1705-3B1C", "07E7-E83A-DAB6",
    "B731-DDB2-6110"
]
def main():
    # Get authenticated service
    #service = get_authenticated_service()
    
    #DATABASE

    service_name = "services/9662-B51E-5089"  # CloudSQL 
    #get_specs(endpoint_url, API_KEY, service_filter, desired_categories, output_file_path)
    #get_prices()
    #combine_json_data(output_file_path, output_file_path2,combined_info)
    #Firestore information
    #fetch_save(API_KEY, 'F17B-412E-CB64',firestore_skus)
    
    #COMPUTE
    #computeinfo()
    
    
    #Getting storage specs
    #get_storage_specs(endpoint_url,API_KEY,service_filter_storage,output_file_Storage)
    # retrieve_prices_from_json(output_file_Storage,API_KEY,storage_combined)
    #fetch_save(API_KEY, '6F81-5844-456A',block_storage_skus) # Block storage, Persistant Disk
    #fetch_save(API_KEY, 'D97E-AB26-5D95',filestore_skus) # Cloud File Store 
    
    
    #NETWORKING
    fetch_save(API_KEY,'E505-1604-58F8',loadbalacer_skus)
   
# Getting the price for CloudSQL services
def get_prices():
    try:
        # Send GET request to the API endpoint with API key as parameter
        response = requests.get(endpoint_url2, params={"key": API_KEY})

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Initialize a list to store formatted data
            formatted_skus = []

            # Extract pricing information
            skus = data.get('skus', [])

            # Format and append each SKU to the list
            for sku in skus:
                formatted_sku = {
                    "Name": sku['name'],
                    "Description": sku['description'],
                    "Pricing_info": sku['pricingInfo']
                }
                formatted_skus.append(formatted_sku)

            # Save the formatted information to a JSON file
            with open(output_file_path2, 'w') as json_file:
                json.dump(formatted_skus, json_file, indent=2)

            print('Pricing information saved to price_info.json')

        else:
            print(f"Error: {response.status_code} - {response.reason}")

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
# Getting specs for Cloud SQL
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
    # Save the formatted response to a JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(filtered_skus, json_file, indent=2)

    print(f'Formatted response saved to {output_file_path}')

# Combining the information from 2 json files for CloudSQL
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

# Moving information for compute from YAML file to DB
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
    
# Getting the storage specs for cloud storage
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

#goes through each one of the skuid in the file and then sends that skuid to the function above to get price and saved t he information into a django database
def retrieve_prices_from_json(json_file, api_key, output_file):
    with open(json_file) as f:
        skus_data = json.load(f)

    combined_data = {}
    for sku_info in skus_data:
        sku_id = sku_info['skuId']
        print("Retrieving prices for SKU ID:", sku_id)
        prices_data = get_google_cloud_sku_prices(sku_id, api_key)
        combined_data[sku_id] = {
            'sku_info': sku_info,
            'prices_data': prices_data
        }

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=2)

    print(f'All SKUs saved to {output_file}')

    # Insert combined information into the database
    for sku_id, data in combined_data.items():
        sku_info = data['sku_info']
        prices_data = data['prices_data']
        
        # Extract relevant information
        name = sku_info.get('displayName', '')
        provider_id = 1  # Assuming you have a default provider with id=1
        cloud_service_id = 1  # Assuming you have a default cloud service with id=1
        tiered_rates = prices_data['prices'][0]['rate']['tiers'][0]
        unit_price_nanos = tiered_rates['listPrice'].get('nanos', 0)
        unit_price_units = tiered_rates['listPrice'].get('units', 0)
        unit_price = unit_price_units + unit_price_nanos / 1000000000
        unit_of_storage = sku_info.get('productTaxonomy', {}).get('taxonomyCategories', [])[4].get('category', '')
        region = sku_info.get('geoTaxonomy', {}).get('regionalMetadata', {}).get('region', {}).get('region', '')
        description = sku_info.get('displayName', '')
        durability = sku_info.get('productTaxonomy', {}).get('taxonomyCategories', [])[4].get('category', '')
        service_code = sku_info.get('geoTaxonomy', {}).get('regionalMetadata', {}).get('region', {}).get('region', '')
        storage_class = sku_info.get('productTaxonomy', {}).get('taxonomyCategories', [])[4].get('category', '')
        volume_type = sku_info.get('productTaxonomy', {}).get('taxonomyCategories', [])[4].get('category', '')
        price_monthly = unit_price
        
        # Insert into StorageSpecifications table
        StorageSpecifications.objects.create(
            name=name,
            provider_id=provider_id,
            cloud_service_id=cloud_service_id,
            sku=sku_id,
            unit_price=unit_price,
            unit_of_storage=unit_of_storage,
            region=region,
            description=description,
            durability=durability,
            service_code=service_code,
            storage_class=storage_class,
            volume_type=volume_type,
            price_monthly=price_monthly
            )

        print(f"Information for SKU ID {sku_id} inserted into the database.")

# def retrieve_prices_from_json(json_file, api_key, output_file):
#     with open(json_file) as f:
#         skus_data = json.load(f)

#     combined_data = {}
#     for sku_info in skus_data:
#         sku_id = sku_info['skuId']
#         print("Retrieving prices for SKU ID:", sku_id)
#         prices_data = get_google_cloud_sku_prices(sku_id, api_key)
#         combined_data[sku_id] = {
#             'sku_info': sku_info,
#             'prices_data': prices_data
#         }
#         with open(output_file, 'w') as outfile:
#             json.dump(combined_data, outfile, indent=2)

#         print(f'All SKUs saved to {output_file}')     

def fetch_save(api_key, service_id, all_skus):
    all_skus = set(all_skus)
    skus_saved = []
    page_token = None

    while True:
        url = f"https://cloudbilling.googleapis.com/v1/services/{service_id}/skus?key={api_key}"
        if page_token:
            url += f"&pageToken={page_token}"

        response = requests.get(url)
        if response.status_code == 200:
            api_data = response.json()
            skus = api_data.get('skus', [])
            for sku in skus:
                sku_id = sku.get('skuId')
                if sku_id in all_skus:
                    # Extract relevant information from the SKU
                    name = sku.get('description', '')
                    data_type = sku.get('category', {}).get('usageType', '')
                    pricing_info = sku.get('pricingInfo', [])
                    
                    # Extract the unit price considering the first price unless it's 0, then take the second price
                    unit_price_nanos = pricing_info[0].get('pricingExpression', {}).get('tieredRates', [{}])[0].get('unitPrice', {}).get('nanos', 0)
                    if unit_price_nanos == 0:
                        unit_price_nanos = pricing_info[0].get('pricingExpression', {}).get('tieredRates', [{}])[1].get('unitPrice', {}).get('nanos', 0)
                    
                    unit_price = unit_price_nanos / 1000000000 if unit_price_nanos else 0.0
                    unit_of_storage = sku.get('pricingInfo', [{}])[0].get('pricingExpression', {}).get('usageUnit', '')
                    region = ', '.join(sku.get('serviceRegions', []))
                    description = sku.get('description', '')

                    # Determine where to save the information based on the service ID
                    if service_id == 'F17B-412E-CB64':
                        # Save to DatabaseSpecifications table
                        db_spec = DatabaseSpecifications.objects.create(
                            name=name,
                            data_type=data_type,
                            cloud_service_id=1,
                            sku=sku_id,
                            unit_price=str(unit_price),
                            unit_of_storage=unit_of_storage,
                            region=region,
                            description=description
                            # Add other fields as needed
                        )
                        db_spec.save()
                    elif service_id == '6F81-5844-456A' or service_id == 'D97E-AB26-5D95':
                        # Save to StorageSpecifications table
                        storage_spec = StorageSpecifications.objects.create(
                            sku=sku_id,
                            name=name,
                            provider_id=1,  # Assuming default provider id
                            cloud_service_id=1,  # Assuming default cloud service id
                            unit_price=str(unit_price),
                            unit_of_storage=unit_of_storage,
                            region=region,
                            description=description
                            # Add other fields as needed
                        )
                        storage_spec.save()
                        
                    elif service_id == 'E505-1604-58F8':
                        # Save to StorageSpecifications table
                        network_spec = NetworkingSpecifications.objects.create(
                            sku=sku_id,
                            name=description,  # Insert description as name value
                            provider_id=1,  # Assuming default provider id
                            cloud_service_id=1,  # Assuming default cloud service id
                            unit_price=str(unit_price),
                            unit_of_measure=unit_of_storage,
                            region=region,
                            price_monthly=str(float(unit_price) * 730)  # Assuming a monthly price (30 days)
                            # Add other fields as needed
                        )
                        network_spec.save()

            page_token = api_data.get('nextPageToken')
            if not page_token:
                break
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return
    
    
# def fetch_and_save_blockstorage(api_key, service_id,block_storage_skus):
#     block_storage_skus = set(block_storage_skus)
#     skus_saved = []
#     page_token = None

#     while True:
#         url = f"https://cloudbilling.googleapis.com/v1/services/{service_id}/skus?key={api_key}"
#         if page_token:
#             url += f"&pageToken={page_token}"

#         response = requests.get(url)
#         if response.status_code == 200:
#             api_data = response.json()
#             skus = api_data.get('skus', [])
#             for sku in skus:
#                 sku_id = sku.get('skuId')
#                 if   sku_id in block_storage_skus:
#                     # Extract relevant information from the SKU
#                     name = sku.get('description', '')
#                     service_display_name = sku.get('category', {}).get('serviceDisplayName', '')
#                     resource_family = sku.get('category', {}).get('resourceFamily', '')
#                     resource_group = sku.get('category', {}).get('resourceGroup', '')
#                     usage_type = sku.get('category', {}).get('usageType', '')
#                     service_regions = sku.get('serviceRegions', [])
#                     pricing_info = sku.get('pricingInfo', [])
                    
#                     # Check if pricing_info list is not empty
#                     if pricing_info:
#                         pricing_info = pricing_info[0]
#                         unit_price_nanos = pricing_info.get('pricingExpression', {}).get('tieredRates', [{}])[0].get('unitPrice', {}).get('nanos', 0)
#                         unit_price = unit_price_nanos / 1000000000 if unit_price_nanos else 0.0
#                         effective_time = pricing_info.get('effectiveTime', '')
#                     else:
#                         unit_price = 0.0
#                         effective_time = ''
#                     # Create an if statement that checks which service is being used then use appropriate django table
#                     if service_id == 'F17B-412E-CB64':
#                         #save the information to the Database table 
#                         print("saving to db")
#                         pass 
#                     elif service_id == '6F81-5844-456A':
#                         # Save the information to the database
#                         storage_spec = StorageSpecifications.objects.create(
#                             sku=sku_id,
#                             name=name,
#                             provider_id=1,  # Assuming default provider id
#                             cloud_service_id=1,  # Assuming default cloud service id
#                             unit_price=unit_price,
#                             unit_of_storage=usage_type,
#                             region=service_regions[0] if service_regions else '',
#                             description=name,
#                             durability=resource_group,
#                             service_code=service_regions[0] if service_regions else '',
#                             storage_class=resource_group,
#                             volume_type=resource_group,
#                             price_monthly=unit_price,
#                             # Add more fields as needed
#                         )
#                         storage_spec.save()

#             page_token = api_data.get('nextPageToken')
#             if not page_token:
#                 break
#         else:
#             print(f"Failed to fetch data from API. Status code: {response.status_code}")
#             return

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
     #Going through the region to set the location for query
    city=None
    if location == 'us-central1':
        city= 'Iowa'   #doesnt work for storage, None for Block Storage
    elif location == 'us-east1': # dont use no location for everything
        city= 'South Carolina'
    elif location == 'us-east2':
        location = 'us-east4'
        city= 'Northern Virginia'
    elif location == 'us-east5':
        city= 'Columbus'
    elif location == 'us-south1':
        city= 'Dallas'
    elif location == 'us-west1':
        city= 'Oregon'# None for postgresql 
    elif location == 'us-west2':
        city= 'Los Angeles'
    elif location == 'us-west3':
        city= 'Salt Lake City'
    elif location == 'us-west4':
        city= 'Las Vegas'
    elif location == 'ap-east1':
        location = 'asia-east2'
        city= 'Hong Kong'
    elif location == 'asia-east1':
        city= 'Taiwan' # None for PostgreSQL
    elif location == 'asia-northeast1':
        city= 'Tokyo' # None for PostgreSQLS
    elif location == 'ap-northeast-3':
        location = 'asia-northeast2'
        city= 'Osaka'
    elif location == 'ap-northeast-2':
        location='asia-northeast3'
        city= 'Seoul'
    elif location == 'ap-south-1':
        location = 'asia-south1'
        city= 'Mumbai'
    elif location == 'asia-south2':
        city= 'Delhi'
    elif location == 'asia-southeast1':
        city= 'Singapore'
    elif location == 'asia-southeast2':
        city= 'Jakarta'
    elif location == 'australia-southeast1':
        city= 'Sydney'
    elif location == 'australia-southeast2':
        city= 'Melbourne'
    elif location == 'europe-central2':
        city= 'Warsaw'
    elif location == 'europe-north1':
        city= 'Finland'
    elif location == 'europe-southwest1':
        city= 'Madrid'
    elif location == 'europe-west1':
        city= 'Belgium' #None for PostgreSql Storage
    elif location == 'europe-west2':
        city= 'London'
    elif location == 'europe-west3':
        city= 'Frankfurt'
    elif location == 'europe-west4':
        city= 'Netherlands'
    elif location == 'europe-west6':
        city= 'Zurich'
    elif location == 'europe-west8':
        city= 'Milan'
    elif location == 'europe-west9':
        city= 'Paris'
    elif location == 'me-west1':
        city= 'Tel Aviv'or 'Isreal'  #Isreal Works not Tel for PosgreSQL storage
    elif location == 'northamerica-northeast1':
        city= 'Montréal'
    elif location == 'northamerica-northeast2':
        city= 'Toronto'
    elif location == 'southamerica-east1':
        city= 'São Paulo'
    elif location == 'southamerica-west1':
        city= 'Santiago'
        
    # Compute Logic
    # Retrieve data from the database based on the provided keyword
    compute_name=None
    if expected_cpu == "1vCPU":
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
    # Compute Logic
    compute_total_cost=0
    compute_instance = ComputeSpecifications.objects.filter(provider__name='GCP', name=compute_name, region=location).first()
    compute_total_cost=float(compute_instance.unit_price)*730 
    computed_data['compute'] = {
        'name': compute_instance.name,
        'unit_price': compute_total_cost,
        'cpu': compute_instance.cpu,
        'memory': compute_instance.memory,
        'sku': compute_instance.sku,
        'provider': compute_instance.provider.name,
        'cloud_service': compute_instance.cloud_service.service_type
    }
#----------------------------------------------------------------------------------------------------------------------------------------
    if storage_size=='large':
        storage_size=100000
    elif storage_size=='medium':    
        storage_size = 10000
    elif storage_size=='small':
        storage_size = 1000
    
    query_temp = None
    if cloud_storage == "File Storage":
        if city in ["Oregon", "Iowa", "South Carolina"]:
            query_temp = "Filestore Capacity Basic HDD (Standard) Iowa/South Carolina/Oregon"
        else:
            query_temp = "Filestore Capacity Basic HDD (Standard) %s"

    elif cloud_storage == 'Block Storage':
        query_temp = "Storage PD Capacity in %s"
        
    elif cloud_storage == "Object Storage":
        query_temp = "Standard Storage %s"

    # Check if query_temp and city are both not None
    if query_temp and city:
        if "%s" in query_temp:  # Check if the format specifier exists in the template
            query = query_temp % city  # Perform string formatting if city is provided
        else:
            query = query_temp

        # Query for the first storage instance based on the query_temp
        storage_instance = StorageSpecifications.objects.filter(name__contains=query).first()
        storage_total_price=float(storage_instance.unit_price)* storage_size  #figure out the pricing is done for the storage. Weather it is per gb a month
        if storage_instance:
            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': storage_total_price, #storage_total_price,
                'unit_of_storage': storage_instance.unit_of_storage,
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type
            }
        elif cloud_storage == 'Block Storage':
            # If no results found using the city, default to querying "Storage PD Capacity"
            query_default = "Storage PD Capacity"
            storage_instance_default = StorageSpecifications.objects.filter(name=query_default).first()
            storage_total_price=float(storage_instance_default.unit_price)* storage_size
            if storage_instance_default:
                computed_data['storage'] = {
                    'name': storage_instance_default.name,
                    'unit_price': storage_total_price, #storage_total_price,
                    'unit_of_storage': storage_instance_default.unit_of_storage,
                    'sku': storage_instance_default.sku,
                    'provider': storage_instance_default.provider.name,
                    'cloud_service': storage_instance_default.cloud_service.service_type
                }
            else:
                computed_data['storage'] = None
        else:
            computed_data['storage'] = None
    else:
        # Handle the case where either query_temp or city is None
        computed_data['storage'] = None
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------                    
    # #Database Logic
    if database_size == 'large':
        database_size = 1000
    elif database_size == 'medium':
        database_size = 100
    elif database_size == 'small':
        database_size = 10
        
    query_template=None
    if database_service== 'postgreSQL':
        query_template = "Cloud SQL for PostgreSQL: Regional - Standard storage in %s"
    elif database_service == 'sql':
        # Additional condition for SQL Server databases if city is Oregon
        if city == "Oregon":
            query_template = "Cloud SQL for SQL Server: Regional - Standard storage in Americas"
        else:
            query_template = "Cloud SQL for SQL Server: Regional - Standard storage in %s"
    elif database_service == 'noSQL': # Need to add Code for the firestore. Not working
        query_template= "Cloud Firestore Storage %s"
    
    if query_template:
        if database_service == 'noSQL' and city in ["South Carolina", "Iowa", "Belgium"]:
            query_template = "Cloud Firestore Storage"  
    # Proceed with constructing the query
    if "%s" in query_template:  # Check if the format specifier exists in the template
        query = query_template % city if city else query_template  # Perform string formatting if city is provided
    else:
        query = query_template

    # Query for the first database instance
    database_instance = DatabaseSpecifications.objects.filter(name=query).first()
    database_total_price= float(database_instance.unit_price)*database_size # be sure to change the price in the database, some of the values have not been formated correctly.
    if database_instance:
        computed_data['database'] = {
            'name': database_instance.name,
            'unit_price': database_total_price,
            'unit_of_storage': database_instance.unit_of_storage,   
            'sku': database_instance.sku,
            'data_type': database_instance.data_type,
            'provider': database_instance.provider.name,
            'cloud_service': database_instance.cloud_service.service_type
        }
    else:
        computed_data['database'] = None
        
        
    #Networking Logic
    inbound_lb = None
    outbound_lb = None
    dns_instance = None
    cdn_instance = None
    name = ""

    if scalability == "essential":
        name += "Auto Scaling & Load Balancing"
        inbound_query = f"Regional External Application Load Balancer Inbound Data Processing for {city}"
        inbound_lb= NetworkingSpecifications.objects.filter(name__contains=inbound_query).first()
        outbound_query= f"Regional External Application Load Balancer Outbound Data Processing for {city}"
        outbound_lb= NetworkingSpecifications.objects.filter(name__contains=outbound_query).first()

    else:
        name = ""
    
    if dns_connection == 'Yes':
        name += " DNS"
        dns_query='0CAB-FE26-F2C6'
        dns_instance= NetworkingSpecifications.objects.filter(sku=dns_query).first()
    else:
        name=""
        
    if cdn_connection == 'Yes':
        name += " CDN"
        cdn_query='620D-FE53-4BA9'
        cdn_instance= NetworkingSpecifications.objects.filter(sku=cdn_query).first()
    else :
        name +=""
        
    if inbound_lb or outbound_lb or dns_instance or cdn_instance:
    # Compute total price only for non-null instances
        network_total_price = (float(inbound_lb.unit_price) if inbound_lb else 0) + \
                            (float(outbound_lb.unit_price) if outbound_lb else 0) + \
                            (float(dns_instance.unit_price) if dns_instance else 0) + \
                            (float(cdn_instance.unit_price) if cdn_instance else 0)

        network_total_price*= 730

        sku_components = [component.sku if component else "" for component in [inbound_lb, outbound_lb, dns_instance, cdn_instance]]
        sku_comp = " + ".join(filter(None, sku_components))
        computed_data['networking'] = {
        'name': name,
        'unit_price': network_total_price,
        'sku': sku_comp
    }
    else:
        computed_data['networking'] = None
        
    
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
    plan_monthly_price = compute_total_cost + storage_total_price + database_total_price + network_total_price

    plan_annual_price = float(plan_monthly_price) * 12
    print("Total Monthly Plan Cost: ", plan_monthly_price)
    print("Total Annual Plan Cost: ", plan_annual_price)
    computed_data['monthly'] = round(plan_monthly_price)
    computed_data['annual'] = round("$" + plan_annual_price)

    return computed_data

def callmain(request):
    main()
    return HttpResponse("Main function called successfully.")

if __name__ == "__main__":
    main()

