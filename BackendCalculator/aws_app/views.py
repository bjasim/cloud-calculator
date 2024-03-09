import boto3
import json
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from databaseServer.models import (
    Provider, CloudService, StorageSpecifications, NetworkingSpecifications, 
    DatabaseSpecifications, ComputeSpecifications
)


# from .models import Provider, CloudService, ComputeSpecifications, DatabaseStorageVolume, DatabaseSpecifications, StorageSpecifications
#-----------------------------------------------------------------------------
# 2.  Compute Type:
# How many users do you expect to have accessing your services simultaneously?
# 	( Example ): Drop down
# 1 vCPU  - 2 RAM ( Standard) 
# 2 vCPU  - 4 RAM ( Standard) 
# 4 vCPU  - 16 RAM ( Standard) 
# 8 vCPU  - 32 RAM ( Standard) 
#*****************************************************************************
# ServiceCode= AmazonEC2 sku = "3DG6WFZ5QW4JAAHJ" # 1 vCPU  - 2 RAM ( Standard) 
# ServiceCode= AmazonEC2 sku = "3K59PVQYWBTWXEHT" #2 vCPU  - 4 RAM ( Standard)
# ServiceCode= AmazonEC2 sku = "7WVK4XHSDKCTP5FX" #4 vCPU  - 16 RAM ( Standard)  
# sku = "4QB2537CEAFFV88T" #8 vCPU  - 32 RAM ( Standard) 

#-----------------------------------------------------------------------------
# 3.	Database Type:
# Question: "What type of database services are you looking for?"Relational (SQL)
# NoSQL
# SQL
# No database is required
#*****************************************************************************
# NoSQL: Storage sku = "F3E2EDSYC6ZNW7XP" # $0.25/gb ServiceCode= AmazonDynamoDB
# Instance sku =  price for per read and write requests (1.25 per million requests)
# SQL: Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS
# Instance sku = "MV3A7KKN6HB749EA or PHXMADZ7H8JN3RRW" 8 GiB memory singe AZ or Multi-AZ
# No database is required - skip to next question

#----------------------------------If SQL is selected in the previous question---------------------------
# Question: "What is the expected size of your database?"
# Small (under 500 GB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS
# Medium (1 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS
# Large (2 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS
# Very large (5 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS
#*****************************************************************************
#----------------------------------If NoSQL is selected in the previous question---------------------------
# Question: "What is the expected size of your database?"
# Small (under 500 GB) Storage sku = "F3E2EDSYC6ZNW7XP" # $0.25/gb Example: 500gb * $0.25 = 125 + $3 for read and write requests ServiceCode= AmazonDynamoDB
# Medium (1 TB) Storage sku = "F3E2EDSYC6ZNW7XP" # $0.25/gb Example: 1TB * $0.25 = 250 + $3 for read and write requests ServiceCode= AmazonDynamoDB
# Large (2 TB) Storage sku = "F3E2EDSYC6ZNW7XP" # $0.25/gb Example: 2TB * $0.25 = 500 + $3 for read and write requests ServiceCode= AmazonDynamoDB
# Very large (5 TB) Storage sku = "F3E2EDSYC6ZNW7XP" # $0.25/gb Example: 5TB * $0.25 = 1250 + $3 for read and write requests ServiceCode= AmazonDynamoDB
#*************************************************************************************************
#--------------------------------------Storage Options------------------------------------------------------
# 7. Cloud Storage:
# 7.1 Object Storage (S3) = sku:WP9ANXZGBYYSGJEA $0.022/GB monthly ServiceCode= AmazonS3
# 7.2 File Storage (EFS) = sku:YFV3RHAD3CDDP3VE standard storage general purpose, $0.30 per GB-Mo ServiceCode= AmazonEFS
# 7.3 Block Storage (EBS) = sku: HY3BZPP2B6K8MSJF gp2-general purpose storage 0.10 per GB-Mo ServiceCode= AmazonEC2 and productFamily= Storage
# 7.4 No Storage Required
#--------------------------------------This is getting json for the specified sku variable -----------------------------------------
# sku = "F3E2EDSYC6ZNW7XP"  

# def get_pricing(request):
#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode='AmazonDynamoDB',
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}
#         ],
#         MaxResults=1
#     )

#     if response['PriceList']:
#         # Directly parse and return the price list without any processing.
#         price_data = json.loads(response['PriceList'][0])
#         return HttpResponse(json.dumps(price_data, indent=4), content_type='application/json')
#     else:
#         return HttpResponse(f"No pricing information found for SKU {sku}", content_type='text/plain')
#--------------------------------------------------------------------------------------------------------------------------------------------
# from django.db import IntegrityError

# # Dictionary mapping SKU to Service Code
sku_to_service_code = {
    "3DG6WFZ5QW4JAAHJ": "AmazonEC2",  # 1 vCPU - 2 RAM (Standard)
    "3K59PVQYWBTWXEHT": "AmazonEC2",  # 2 vCPU - 4 RAM (Standard)
    "7WVK4XHSDKCTP5FX": "AmazonEC2",  # 1 vCPU - 2 RAM (Standard)
    "4QB2537CEAFFV88T": "AmazonEC2",  # 2 vCPU - 4 RAM (Standard)
    
    "F3E2EDSYC6ZNW7XP": "AmazonDynamoDB",  # $0.25/gb storage  >>databasestoragevolume table
    "MV3A7KKN6HB749EA": "AmazonRDS",  #8 GiB memory singe AZ SQL Server >>databaseSpecifications table
    "QVD35TA7MPS92RBC": "AmazonRDS",   # SQL   Single-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS >>databasestoragevolume table

    "WP9ANXZGBYYSGJEA": "AmazonS3",  # $$0.022/GB monthly
    "YFV3RHAD3CDDP3VE": "AmazonEFS",  #standard storage general purpose, $0.30 per GB-Mo
    "HY3BZPP2B6K8MSJF": "AmazonEC2",   # gp2-general purpose storage 0.10 per GB-Mo
}
def get_pricing(request):

    # Iterate over each SKU in the sku_to_service_code dictionary
    for sku, service_code in sku_to_service_code.items():
        # Fetch Pricing Data for each SKU
        pricing_data = fetch_pricing_data(sku, service_code)
        if not pricing_data:
            continue

        # Process and Save Data for each SKU
        process_and_save_data(sku, service_code, pricing_data)

    return HttpResponse("All SKUs have been processed.")

    # sku = request.GET.get('sku')
    # if not sku:
    #     return HttpResponse("SKU parameter is missing", status=400)

    # service_code = sku_to_service_code.get(sku)
    # if not service_code:
    #     return HttpResponse(f"Service code not found for SKU {sku}", status=404)

    # # Fetch Pricing Data
    # pricing_data = fetch_pricing_data(sku, service_code)
    # if not pricing_data:
    #     return HttpResponse(f"No pricing data found for SKU {sku}", status=404)

    # # Process and Save Data
    # process_and_save_data(sku, service_code, pricing_data)

    # return JsonResponse(pricing_data, safe=False, json_dumps_params={'indent': 4})

def fetch_pricing_data(sku, service_code):
    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode=service_code,
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}],
        MaxResults=1
    )
    if response['PriceList']:
        return json.loads(response['PriceList'][0])
    return None


# def process_ec2_data(sku, pricing_data):
#     # AWS Provider and Compute CloudService setup
#     provider_name = 'AWS'
#     provider, _ = Provider.objects.get_or_create(name=provider_name)

#     cloud_service_type = 'Compute'
#     cloud_service, _ = CloudService.objects.get_or_create(
#         provider=provider, 
#         service_type=cloud_service_type,
#         defaults={'description': 'AWS EC2 Service'}
#     )
    

#     # EC2 specific data extraction
#     attributes = pricing_data.get('product', {}).get('attributes', {})
#     instance_type = attributes.get('instanceType', 'No type provided.')
#     operating_system = attributes.get('operatingSystem', 'Ubuntu Pro')
#     cpu = attributes.get('vcpu', 'Not specified')
#     memory = attributes.get('memory', 'Not specified')
#     network_performance = attributes.get('networkPerformance', 'No network provided.')
#     tenancy = attributes.get('tenancy', 'Not specified')

#     # Extract price and description
#     price_list = pricing_data.get('terms', {}).get('OnDemand', {})
#     for sku_details in price_list.values():
#         for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
#             description = offer_term_details.get('description', 'No description provided.')
#             price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD')
            
#             # Update or create new ComputeSpecifications entry
#             compute_spec, created = ComputeSpecifications.objects.update_or_create(
#                 sku=sku,
#                 defaults={
#                     'provider': provider,
#                     'cloud_service': cloud_service,
#                     'instance_type': instance_type,
#                     'operating_system': operating_system,
#                     'cpu': cpu,
#                     'memory': memory,
#                     'network_performance': network_performance,
#                     'tenancy': tenancy,
#                     'description': description,
#                     'unit_price': price_per_unit or 0.0,
#                     'currency': 'USD'
#                 }
#             )
#             print(f"New data created for SKU: {sku}")
#             break
#         break

#     return HttpResponse("AWS data processed successfully.")
def process_ec2_data(sku, pricing_data, region):
    # AWS Provider and Compute CloudService setup
    provider_name = 'AWS'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Compute'
    cloud_service, _ = CloudService.objects.get_or_create(
        provider=provider, 
        service_type=cloud_service_type,
        defaults={'description': 'AWS EC2 Service'}
    )

    # EC2 specific data extraction
    attributes = pricing_data.get('product', {}).get('attributes', {})
    instance_type = attributes.get('instanceType', 'No type provided.')
    operating_system = attributes.get('operatingSystem', 'Ubuntu Pro')
    cpu = attributes.get('vcpu', None)
    memory = attributes.get('memory', None)
    region = attributes.get('location', 'Not specified')

    if cpu is not None and memory is not None and memory != 'NA':
        try:
            cpu_value = int(cpu)
            memory_value = float(memory.split()[0])  # Extract numeric part of memory and convert to float
        except ValueError:
            print(f"Invalid data for SKU: {sku}, skipping.")
            return  # Skip this record


        # Check if the instance matches the criteria
        if cpu_value <= 16 and memory_value <= 64:
            # Extract price and description
            price_list = pricing_data.get('terms', {}).get('OnDemand', {})
            for sku_details in price_list.values():
                for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
                    description = offer_term_details.get('description', 'No description provided.')
                    price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD')

                    # Update or create new ComputeSpecifications entry
                    compute_spec, created = ComputeSpecifications.objects.update_or_create(
                        sku=sku,
                        defaults={
                            'provider': provider,
                            'cloud_service': cloud_service,
                            'instance_type': instance_type,
                            'operating_system': operating_system,
                            'cpu': cpu,
                            'memory': memory,
                            'network_performance': attributes.get('networkPerformance', 'No network provided.'),
                            'tenancy': attributes.get('tenancy', 'Not specified'),
                            'description': description,
                            'unit_price': price_per_unit or 0.0,
                            'currency': 'USD',
                            'region': region  # Saving the region information
                        }
                    )
                    print(f"New data created for SKU: {sku} in region: {region}")
                    break
                break
        else:
            print(f"Skipping SKU: {sku} as it does not meet the criteria.")
    else:
        print(f"CPU or memory information missing for SKU: {sku}. Skipping.")

    return HttpResponse("AWS data processed successfully.")


def process_to_database_storage_specification(sku, pricing_data):
    provider_name = 'AWS'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Database'
    cloud_service, _ = CloudService.objects.get_or_create(
        provider=provider, 
        service_type=cloud_service_type,
        defaults={'description': 'AWS Database Service'}
    )

    product_attributes = pricing_data.get('product', {}).get('attributes', {})
    volume_type = product_attributes.get('volumeType', "No type provided.")
    storage_capacity = product_attributes.get('storage', "Inf")

    # Extracting the terms, description, and price
    terms = pricing_data.get('terms', {})
    on_demand = terms.get('OnDemand', {})
    description = "No description provided."
    price_per_unit = None  # Initialize as None to check if a valid price is found
    price_count = 0  # Counter to skip the first price (free tier)

    for sku_details in on_demand.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            temp_price = offer_term_details.get('pricePerUnit', {}).get('USD', "0.0")
            # Parse the price as a float and check if it's the first valid price or a non-zero price
            temp_price_float = float(temp_price)
            if price_per_unit is None or (price_per_unit == 0.0 and temp_price_float != 0.0):
                price_per_unit = temp_price_float
                description = offer_term_details.get('description', description)

    # Check if a record with the given SKU exists
    try:
        storage_volume = DatabaseSpecifications.objects.get(sku=sku)
        # If the record exists, update it with the new details
        created = False
    except DatabaseSpecifications.DoesNotExist:
        # If the record does not exist, create a new one
        storage_volume = DatabaseSpecifications(
            provider=provider,  # Assign the AWS provider
            cloud_service=cloud_service,  # Assign the AWS Database service 
            unit_price=price_per_unit or 0.0,
            sku=sku,
            description=description,
            volume_type=volume_type,
            storage_capacity=storage_capacity,
        )
        created = True

    # Save or update the record
    storage_volume.sku = sku
    storage_volume.storage_capacity = storage_capacity
    storage_volume.description = description
    storage_volume.volume_type = volume_type
    storage_volume.storage_capacity = storage_capacity
    formatted_price = "{:.4f}".format(price_per_unit)
    storage_volume.volume_price = formatted_price
    storage_volume.save()

    print(f"Data {'created' if created else 'updated'} for SKU: {sku}")

    # Verification Query
    try:
        verify_volume = DatabaseSpecifications.objects.get(sku=sku)
        print(f"Verification: Found SKU: {storage_volume.sku}, Price: {storage_volume.unit_price}, Volume Type: {storage_volume.volume_type}")
    except DatabaseSpecifications.DoesNotExist:
        print(f"Verification Failed: SKU {sku} not found in database.")



def process_to_database_specifications(sku, pricing_data):
    provider_name = 'AWS'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Database'
    cloud_service, _ = CloudService.objects.get_or_create(
        provider=provider, 
        service_type=cloud_service_type,
        defaults={'description': 'AWS Database Service'}
    )

    product = pricing_data.get('product', {}).get('productFamily', {})
    attributes = pricing_data.get('product', {}).get('attributes', {})
    instance_type = attributes.get('instanceType', 'Not specified')
    database_engine = attributes.get('databaseEngine')
    cpu = attributes.get('vcpu', 'Not specified')
    memory = attributes.get('memory', 'Not specified')
    network_performance = attributes.get('networkPerformance', 'Not specified')

    # Default values
    description = ''
    price_per_unit = '0.0'

    price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    for sku_details in price_list.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            description = offer_term_details.get('description', description)
            price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD', price_per_unit)

    try:
        database_specifications = DatabaseSpecifications.objects.get(sku=sku)
        created = False
    except DatabaseSpecifications.DoesNotExist:
        database_specifications = DatabaseSpecifications(
            provider=provider,  # Assign the AWS provider
            cloud_service=cloud_service,  # Assign the AWS Database service
            product=product,
            sku=sku,
            instance_type=instance_type,
            db_engine=database_engine,
            cpu=cpu,
            memory=memory,
            network_performance=network_performance,
            description=description,
            unit_price=price_per_unit,
        )
        created = True


    database_specifications.product = product
    database_specifications.sku = sku
    database_specifications.db_engine = database_engine
    database_specifications.cpu = cpu
    database_specifications.memory = memory
    database_specifications.network_performance = network_performance
    database_specifications.description = description
    database_specifications.instance_type = instance_type

    # Safely convert price_per_unit to float
    try:
        formatted_price = "{:.4f}".format(float(price_per_unit))
    except ValueError:
        formatted_price = "0.0000"

    database_specifications.instance_price = formatted_price
    database_specifications.save()

    print(f"Data {'created' if created else 'updated'} for SKU: {sku}")

    # Verification Query
    try:
        verify_volume = DatabaseSpecifications.objects.get(sku=sku)
        print(f"Verification: Found SKU: {database_specifications.sku}, Price: {database_specifications.unit_price}, Volume Type: {database_specifications.volume_type}")
    except DatabaseSpecifications.DoesNotExist:
        print(f"Verification Failed: SKU {sku} not found in database.")


def process_to_storage_specifications(sku, pricing_data):
    # Extracting initial attributes
    provider_name = 'AWS'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Storage'
    cloud_service, _ = CloudService.objects.get_or_create(
        provider=provider, 
        service_type=cloud_service_type,
        defaults={'description': 'AWS Storage Service'}
    )

    product_attributes = pricing_data.get('product', {}).get('attributes', {})
    volume_type = product_attributes.get('volumeType', "No volume type provided.")
    storage_class = product_attributes.get('storageClass', "No storage class provided.")
    durability = product_attributes.get('durability', "No durability provided.")
    service_code = product_attributes.get('servicecode', "No service code provided.")

    # Extracting the terms, description, and price
    terms = pricing_data.get('terms', {})
    on_demand = terms.get('OnDemand', {})
    description = "No description provided."
    price = "No price provided."
    unit = "No unit provided."

    # found_first = False  # Flag to indicate if the first item has been processed
    price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    for sku_details in price_list.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            description = offer_term_details.get('description', description)
            price = offer_term_details.get('pricePerUnit', {}).get('USD', price)
            # unit = offer_term_details.get('unit', unit)



    # Check if a record with the given SKU exists

    try:
        storage_specifications = StorageSpecifications.objects.get(sku=sku)
        created = False
    except StorageSpecifications.DoesNotExist:
        storage_specifications = StorageSpecifications(
            provider=provider,  # Assign the AWS provider
            cloud_service=cloud_service,  # Assign the AWS Storage service
            sku=sku,
            description=description,
            durability=durability,
            volume_type=volume_type,
            service_code=service_code,
            storage_class=storage_class,
            unit_price=price or 0.0,
        )
        created = True

    # Save or update the record
    storage_specifications.sku=sku
    storage_specifications.description = description
    storage_specifications.durability = durability
    storage_specifications.volume_type = volume_type
    storage_specifications.service_code = service_code
    storage_specifications.storage_class = storage_class
    formatted_price = "{:.4f}".format(float(price))
    storage_specifications.price = formatted_price
    storage_specifications.save()

    print(f"Data {'created' if created else 'updated'} for SKU: {sku}")

    # Verification Query
    try:
        verify_volume = StorageSpecifications.objects.get(sku=sku)
        print(f"Verification: Found SKU: {sku}, Price: {price}, Volume Type: {volume_type}")
    except StorageSpecifications.DoesNotExist:
        print(f"Verification Failed: SKU {sku} not found in database.")


def process_and_save_data(sku, service_code, pricing_data):
    # Check if SKU is part of AmazonEC2 and not "HY3BZPP2B6K8MSJF"
    if service_code == "AmazonEC2" and sku != "HY3BZPP2B6K8MSJF":
        process_ec2_data(sku, pricing_data)
    elif service_code == "AmazonDynamoDB" or sku == "QVD35TA7MPS92RBC":
        # Call the process_dynamodb_data function for DynamoDB SKUs
        process_to_database_storage_specification(sku, pricing_data)
    elif sku == "MV3A7KKN6HB749EA":
        process_to_database_specifications(sku, pricing_data)
    elif service_code == "AmazonS3" or service_code == "AmazonEFS" or sku == "HY3BZPP2B6K8MSJF":
        process_to_storage_specifications(sku, pricing_data)
    else:
        # Handle other cases or simply pass
        pass

    # Return the original pricing_data for the Django view
    return pricing_data



#----------------------------------------------------------------------------------------------------
def aws_compute_fetch(request):
    client = boto3.client('pricing', region_name='us-east-1')
    # max_records = 500
    regions = [
        'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'af-south-1',
    ]
    
    records_processed = 0

    for region in regions:
        records_processed = 0
        response = client.get_products(
            ServiceCode='AmazonEC2',
            Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': region}],
            MaxResults=100
        )
    # response = client.get_products(
    #     ServiceCode='AmazonEC2',
    #     Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
    #     MaxResults=100
    # )

    # Pass the process_ec2_data function as an argument
   
        records_processed += process_aws_pricing_data(response, process_ec2_data, region)
        while 'NextToken' in response and records_processed:
            response = client.get_products(
                ServiceCode='AmazonEC2',
                Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': region}],
                MaxResults=100,
                NextToken=response['NextToken']
            )
            records_processed += process_aws_pricing_data(response, process_ec2_data, region)

    # while 'NextToken' in response and records_processed < max_records:
    #     response = client.get_products(
    #         ServiceCode='AmazonEC2',
    #         Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-west-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-west-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'af-south-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-east-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-south-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-southeast-3'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-southeast-4'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-south-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-northeast-3'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-northeast-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-southeast-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-southeast-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-northeast-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ca-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ca-west-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-west-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-west-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-south-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-west-3'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-south-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-north-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'eu-central-2'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-south-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'sa-east-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-gov-east-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-gov-west-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],
    #         # Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'me-central-1'}],

    #         MaxResults=100,
    #         NextToken=response['NextToken']
    #     )
    #     # Again, pass the process_ec2_data function
        # records_processed += process_aws_pricing_data(response, process_ec2_data)
        print(f"Processed {records_processed} records for region: {region}")

    return JsonResponse({"message": "AWS EC2 data processed for all regions"}, safe=False)
#----------------------------------------------------------------------------------------------------------------------
def aws_storage_fetch(request):
    client = boto3.client('pricing', region_name='us-east-1')
    max_records = 500
    records_processed = 0

    response = client.get_products(
        ServiceCode='AmazonS3',  # change as needed for other services
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}
        ],
        MaxResults=100
    )

    records_processed += process_aws_pricing_data(response, process_to_storage_specifications)

    # Handle pagination
    while 'NextToken' in response and records_processed < max_records:
        response = client.get_products(
            ServiceCode='AmazonS3',  
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}
            ],
            MaxResults=100,
            NextToken=response['NextToken']
        )
        records_processed += process_aws_pricing_data(response, process_to_storage_specifications)

    return JsonResponse({"message": f"AWS Storage data processed. Total records: {records_processed}"}, safe=False)
#--------------------------------------------------------------------------------------------------------------------------
def aws_rds_fetch(request):
    client = boto3.client('pricing', region_name='us-east-1')
    max_records = 500
    records_processed = 0

    response = client.get_products(
        ServiceCode='AmazonRDS',
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
        MaxResults=100
    )

    records_processed += process_aws_pricing_data(response, process_to_database_specifications)

    while 'NextToken' in response and records_processed < max_records:
        response = client.get_products(
            ServiceCode='AmazonRDS',
            Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
            MaxResults=100,
            NextToken=response['NextToken']
        )
        records_processed += process_aws_pricing_data(response, process_to_database_specifications)

    return JsonResponse({"message": f"AWS RDS data processed. Total records: {records_processed}"}, safe=False)



#---------------------------------------------------------------------------------------------------------------------------
def aws_networking_fetch(request, service_code):
    client = boto3.client('pricing', region_name='us-east-1')
    max_records = 500
    records_processed = 0

    response = client.get_products(
        ServiceCode=service_code,  # Use the provided service code
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
        MaxResults=100
    )

    records_processed += process_aws_pricing_data(response, process_networking_data)

    while 'NextToken' in response and records_processed < max_records:
        response = client.get_products(
            ServiceCode=service_code,  # Consistent service code
            Filters=[{'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'}],
            MaxResults=100,
            NextToken=response['NextToken']
        )
        records_processed += process_aws_pricing_data(response, process_networking_data)

    return JsonResponse({"message": f"AWS {service_code} data processed. Total records: {records_processed}"}, safe=False)


def process_networking_data(sku, pricing_data):
    provider_name = 'AWS'
    provider, _ = Provider.objects.get_or_create(name=provider_name)

    cloud_service_type = 'Networking'
    cloud_service, _ = CloudService.objects.get_or_create(
        provider=provider,
        service_type=cloud_service_type,
        defaults={'description': 'AWS Networking Service'}
    )
    service_code = pricing_data.get('product', {}).get('attributes', {}).get('servicecode', 'Not specified')
    price_per_unit = '0.0'

    price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    for sku_details in price_list.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD', price_per_unit)

    try:
        networking_spec = NetworkingSpecifications.objects.get(sku=sku)
    except NetworkingSpecifications.DoesNotExist:
        networking_spec = NetworkingSpecifications(
            provider=provider,
            cloud_service=cloud_service,
            sku=sku,
            # service_code=service_code,
            unit_price=price_per_unit or 0.0,
        )
        networking_spec.save()
        print(f"New data created for SKU: {sku}")

def aws_route53_fetch(request):
    return aws_networking_fetch(request, "AmazonRoute53")

def aws_direct_fetch(request):
    return aws_networking_fetch(request, "AWSDirectConnect")

def aws_cloudfront_fetch(request):
    return aws_networking_fetch(request, "AmazonCloudFront")
def aws_vpc_fetch(request):
    return aws_networking_fetch(request, "AmazonVPC")




# def process_aws_pricing_data(response, process_function):
#     processed = 0
#     for price_str in response['PriceList']:
#         try:
#             pricing_data = json.loads(price_str)
#             sku = pricing_data.get('product', {}).get('sku')
#             if sku:
#                 process_function(sku, pricing_data)
#                 processed += 1
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#     return processed

def process_aws_pricing_data(response, process_function, region):
    processed = 0
    for price_str in response['PriceList']:
        try:
            pricing_data = json.loads(price_str)
            sku = pricing_data.get('product', {}).get('sku')
            if sku:
                process_function(sku, pricing_data, region)  # Pass the region to the processing function
                processed += 1
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
    return processed


def calculated_data_AWS(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    computed_data = {'provider': 'AWS',}  # Initialize dictionary to store computed data
    # print(f"database size is:  {database_size}")
    if expected_cpu:
        if expected_cpu == "1vCPU":
            compute_sku = "3DG6WFZ5QW4JAAHJ"
        elif expected_cpu == "2vCPUs":
            compute_sku = '3K59PVQYWBTWXEHT'
        elif expected_cpu == "4vCPUs":
            compute_sku = '7WVK4XHSDKCTP5FX'
        elif expected_cpu == "8vCPUs":
            compute_sku = '4QB2537CEAFFV88T'
        # else:
        #     compute_sku = '4QB2537CEAFFV88T'



        # Fetch the compute instance with the specific SKU
        try:
            compute_instance = ComputeSpecifications.objects.get(sku=compute_sku, provider__name='AWS')
            # unit_price = float(compute_instance.unit_price) * 720 # Convert unit price to float
            compute_unit_price = float(compute_instance.unit_price)# Convert unit price to float

            computed_data['compute'] = {
                'name': compute_instance.name,
                # 'unit_price': unit_price,
                'unit_price': compute_unit_price,
                'cpu': compute_instance.cpu,
                'memory': compute_instance.memory,
                'sku': compute_instance.sku,
                'provider': compute_instance.provider.name,
                'cloud_service': compute_instance.cloud_service.service_type,
                'description': compute_instance.description  # Assuming there's a description field
            }        
            # compute_total_price = unit_price  # Calculate total price
            compute_total_price = compute_unit_price * 720  # Calculate total price
            print("-------------------------------------------------------------")
            print(f"Compute unit price is:  {compute_unit_price}")
            print(f"Compute total price is:  {compute_total_price}")

        except ComputeSpecifications.DoesNotExist:
            computed_data['compute'] = 'No compute instance found for SKU 3DG6WFZ5QW4JAAHJ.'

        #--------------------------------------Storage Options------------------------------------------------------
# 7. Cloud Storage:
# 7.1 Object Storage (S3) = sku:WP9ANXZGBYYSGJEA $0.022/GB monthly ServiceCode= AmazonS3
# 7.2 File Storage (EFS) = sku:YFV3RHAD3CDDP3VE standard storage general purpose, $0.30 per GB-Mo ServiceCode= AmazonEFS
# 7.3 Block Storage (EBS) = sku: HY3BZPP2B6K8MSJF gp2-general purpose storage 0.10 per GB-Mo ServiceCode= AmazonEC2 and productFamily= Storage
# 7.4 No Storage Required

    if cloud_storage:
        if cloud_storage == "Object Storage":
            storage_sku = "WP9ANXZGBYYSGJEA"
        elif cloud_storage == "File Storage":
            storage_sku = 'YFV3RHAD3CDDP3VE'
        elif cloud_storage == "Block Storage":
            storage_sku = 'HY3BZPP2B6K8MSJF'
        # elif cloud_storage == "No Storage":
        #     storage_sku = '3K59PVQYWBTWXEHT'
       
        # Query for the first storage instance based on the keyword "File"
        storage_instance = StorageSpecifications.objects.get(sku=storage_sku, provider__name='AWS')
        storage_unit_price = float(storage_instance.unit_price)# Convert unit price to float
        # db_storage_total_price = db_storage_unit_price * db_size

        if storage_instance:
            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': storage_unit_price,
                'unit_of_storage': storage_instance.unit_of_storage,
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type
            }
        print("-------------------------------------------------------------")
        print(f"Storage unit price is:  {storage_unit_price}")
        # print(f"Storage total price is:  {storage_total_price}")

        
    if database_service:
        if database_service == 'noSQL':
            db_sku = 'F3E2EDSYC6ZNW7XP' # just multiply by the size they need , dynamoDB
        elif database_service == 'sql':
            db_sku = 'QVD35TA7MPS92RBC' # multiply with the size they need , and add instance price'
            db_instance_sku = 'MV3A7KKN6HB749EA'
            try:
                database_instance = DatabaseSpecifications.objects.get(sku=db_instance_sku, provider__name='AWS')
                db_instance_unit_price = float(database_instance.unit_price)# Convert unit price to float
                db_instance_total_price = db_instance_unit_price * 720  # Calculate total price

                # computed_data['database'] = {
                #     'name': database_instance.name,
                #     'unit_price': db_unit_price,
                #     'unit_of_storage': database_instance.unit_of_storage,
                #     'sku': database_instance.sku,
                #     'data_type': database_instance.data_type,
                #     'provider': database_instance.provider.name,
                #     'cloud_service': database_instance.cloud_service.service_type
                # }
                # database_total_price = db_unit_price * db_size
                # print(f"Database total price is:  {database_total_price}")
                print("-------------------------------------------------------------")
                print(f"DB Instance total price:  {db_instance_unit_price}")
                print(f"DB Instance total price:  {db_instance_total_price}")

            except DatabaseSpecifications.DoesNotExist:
                computed_data['database'] = 'No database instance found for SKU fsdfsdfsdfsdfsd.'

        # elif: 
        #     break            
    if database_size:     
        if database_size == 'small':
            db_size = 1000
        elif database_size == 'medium':
            db_size = 5000
        elif database_size == 'large':
            db_size = 10000
        elif database_size == 'veryLarge':
            db_size = 100000
        # else:
        #     db_size = 10

        try:
            database_instance = DatabaseSpecifications.objects.get(sku=db_sku, provider__name='AWS')
            db_storage_unit_price = float(database_instance.unit_price)# Convert unit price to float

            computed_data['database'] = {
                    'name': database_instance.name,
                    'unit_price': db_storage_unit_price,
                    'unit_of_storage': database_instance.unit_of_storage,
                    'sku': database_instance.sku,
                    'data_type': database_instance.data_type,
                    'provider': database_instance.provider.name,
                    'cloud_service': database_instance.cloud_service.service_type
                }
            db_storage_total_price = db_storage_unit_price * db_size
            print("-------------------------------------------------------------")
            print(f"Database storage unit price is:  {db_storage_unit_price}")
            print(f"Database storage total price is:  {db_storage_total_price}")

        except DatabaseSpecifications.DoesNotExist:
            computed_data['database'] = 'No database instance found for SKU fsdfsdfsdfsdfsd.'
        print("--------------------------------------------------------------")

    # Combine total prices if both instance and storage are used
    if database_service == 'sql':
        total_db_price = db_instance_total_price + db_storage_total_price
        print("Total database cost (instance + storage): ", total_db_price)
    else:
        total_db_price = db_storage_total_price
        print("Total database cost (only storage): ", total_db_price)

    


            

        
        
        # Query for the first database instance
        # database_instance = DatabaseSpecifications.objects.get(sku=compute_sku, provider__name='AWS')
        # if database_instance:
        #     computed_data['database'] = {
        #         'name': database_instance.name,
        #         'unit_price': database_instance.unit_price,
        #         'unit_of_storage': database_instance.unit_of_storage,
        #         'sku': database_instance.sku,
        #         'data_type': database_instance.data_type,
        #         'provider': database_instance.provider.name,
        #         'cloud_service': database_instance.cloud_service.service_type
        #     }
        # else:
        #     computed_data['database'] = None
            
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
    plan_monthly_price = compute_total_price + storage_unit_price + total_db_price
    # plan_monthly_price = compute_total_price + storage_unit_price

    plan_annual_price = float(plan_monthly_price) * 12
    print("Total Monthly Plan Cost: ", plan_monthly_price)
    print("Total Annual Plan Cost: ", plan_annual_price)

    computed_data['monthly'] = plan_monthly_price
    computed_data['annual'] = plan_annual_price




    return computed_data



# # to-do
# do logic for storage
# calculate for storage
# Show monthly and annual prices in the front-end UI
# Add question for storage size
# # implement the same functionality for rds as the networking services and pass service code to the function to fetch data trhough API (S3, EFS, etc..)