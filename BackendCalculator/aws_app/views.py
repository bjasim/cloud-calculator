import boto3
import json
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse, HttpResponse


from .models import Provider, CloudService, ComputeSpecifications, DatabaseStorageVolume, DatabaseSpecifications, StorageSpecifications
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
from django.db import IntegrityError

# Dictionary mapping SKU to Service Code
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
    sku = request.GET.get('sku')
    if not sku:
        return HttpResponse("SKU parameter is missing", status=400)

    service_code = sku_to_service_code.get(sku)
    if not service_code:
        return HttpResponse(f"Service code not found for SKU {sku}", status=404)

    # Fetch Pricing Data
    pricing_data = fetch_pricing_data(sku, service_code)
    if not pricing_data:
        return HttpResponse(f"No pricing data found for SKU {sku}", status=404)

    # Process and Save Data
    process_and_save_data(sku, service_code, pricing_data)

    return JsonResponse(pricing_data, safe=False, json_dumps_params={'indent': 4})

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


def process_ec2_data(sku, pricing_data):
    # EC2 specific data extraction
    attributes = pricing_data.get('product', {}).get('attributes', {})
    instance_type = attributes.get('instanceType', 'No type provided.')
    operating_system = attributes.get('operatingSystem', 'Ubuntu Pro')
    cpu = attributes.get('vcpu', 'Not specified')
    memory = attributes.get('memory', 'Not specified')
    network_performance = attributes.get('networkPerformance', 'No network provided.')
    tenancy = attributes.get('tenancy', 'Not specified')

    # Extract price and description
    price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    for sku_details in price_list.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            description = offer_term_details.get('description', 'No description provided.')
            price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD')

            # Check if a record with the given SKU exists
            try:
                compute_spec = ComputeSpecifications.objects.get(sku=sku)
                # If the record exists, update it with the new details
                created = False
            except ComputeSpecifications.DoesNotExist:
                # If the record does not exist, create a new one
                compute_spec = ComputeSpecifications(
                    sku=sku,
                    instance_type=instance_type,
                    operating_system=operating_system,
                    cpu=cpu,
                    memory=memory,
                    network_performance=network_performance,
                    tenancy=tenancy,
                    description=description,
                    price_per_unit=price_per_unit or 0.0,
                    currency='USD'
                )
                created = True
            
            # Save or update the record
            compute_spec.instance_type = instance_type
            compute_spec.operating_system = operating_system
            compute_spec.cpu = cpu
            compute_spec.memory = memory
            compute_spec.network_performance = network_performance
            compute_spec.tenancy = tenancy
            compute_spec.description = description
            compute_spec.price_per_unit = price_per_unit or 0.0
            compute_spec.save()

            print(f"Data {'created' if created else 'updated'} for SKU: {sku}")

            # Verification Query
            try:
                verify_spec = ComputeSpecifications.objects.get(sku=sku)
                print(f"Verification: Found SKU: {verify_spec.sku}, Price: {verify_spec.price_per_unit}, Network Performance: {verify_spec.network_performance}")
            except ComputeSpecifications.DoesNotExist:
                print(f"Verification Failed: SKU {sku} not found in database.")

            break  # Assuming we need the first found description and price
        break  # Exiting after processing the first SKU details

def process_to_database_storage(sku, pricing_data):
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
        storage_volume = DatabaseStorageVolume.objects.get(volume_sku=sku)
        # If the record exists, update it with the new details
        created = False
    except DatabaseStorageVolume.DoesNotExist:
        # If the record does not exist, create a new one
        storage_volume = DatabaseStorageVolume(
            volume_sku=sku,
            description=description,
            volume_type=volume_type,
            storage_capacity=storage_capacity,
            volume_price=price_per_unit or 0.0,
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
        verify_volume = DatabaseStorageVolume.objects.get(volume_sku=sku)
        print(f"Verification: Found SKU: {storage_volume.volume_sku}, Price: {storage_volume.volume_price}, Volume Type: {storage_volume.volume_type}")
    except DatabaseStorageVolume.DoesNotExist:
        print(f"Verification Failed: SKU {sku} not found in database.")



def process_to_database_specifications(sku, pricing_data):
    product = pricing_data.get('product', {}).get('productFamily', {})
    attributes = pricing_data.get('product', {}).get('attributes', {})
    instance_type = attributes.get('instanceType')
    database_engine = attributes.get('databaseEngine')
    cpu = attributes.get('vcpu')
    memory = attributes.get('memory')
    network_performance = attributes.get('networkPerformance')

    # Default values
    description = ''
    price_per_unit = '0.0'

    price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    for sku_details in price_list.values():
        for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
            description = offer_term_details.get('description', description)
            price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD', price_per_unit)

    try:
        database_specifications = DatabaseSpecifications.objects.get(instance_sku=sku)
        created = False
    except DatabaseSpecifications.DoesNotExist:
        database_specifications = DatabaseSpecifications(
            product=product,
            instance_sku=sku,
            instance_type=instance_type,
            db_engine=database_engine,
            cpu=cpu,
            memory=memory,
            network_performance=network_performance,
            description=description,
            instance_price=price_per_unit,
        )
        created = True


    database_specifications.product = product
    database_specifications.instance_sku = sku
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
        verify_volume = DatabaseStorageVolume.objects.get(volume_sku=sku)
        print(f"Verification: Found SKU: {database_specifications.volume_sku}, Price: {database_specifications.volume_price}, Volume Type: {database_specifications.volume_type}")
    except DatabaseStorageVolume.DoesNotExist:
        print(f"Verification Failed: SKU {sku} not found in database.")


def process_to_storage_specifications(sku, pricing_data):
    # Extracting initial attributes
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
        # If the record exists, update it with the new details
        created = False
    except StorageSpecifications.DoesNotExist:
        # If the record does not exist, create a new one
        storage_specifications = StorageSpecifications(
            sku=sku,
            description=description,
            durability=durability,
            volume_type=volume_type,
            service_code=service_code,
            storage_class=storage_class,
            price=price or 0.0,
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
        process_to_database_storage(sku, pricing_data)
    elif sku == "MV3A7KKN6HB749EA":
        process_to_database_specifications(sku, pricing_data)
    elif service_code == "AmazonS3" or service_code == "AmazonEFS" or sku == "HY3BZPP2B6K8MSJF":
        process_to_storage_specifications(sku, pricing_data)
    else:
        # Handle other cases or simply pass
        pass

    # Return the original pricing_data for the Django view
    return pricing_data


# specify each sku and the serviceCode for it --------------------------
# Call the api with sku and service cod --------------------------------
# Create functions to store "MV3A7KKN6HB749EA" and storage information into tables based on SKUs, just like compute is done
# store/update to the tables with sku information (automate those three steps every morning)
# get submitted form and make backend logic for it

