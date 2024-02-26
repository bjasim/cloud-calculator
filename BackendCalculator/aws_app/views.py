
import boto3
import json
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse, HttpResponse


from .models import Provider, CloudService, ComputeSpecifications
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
    
    "F3E2EDSYC6ZNW7XP": "AmazonDynamoDB",  # $0.25/gb storage
    "MV3A7KKN6HB749EA": "AmazonRDS",  #8 GiB memory singe AZ SQL Server
    "QVD35TA7MPS92RBC": "AmazonRDS",   # SQL   Single-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS

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


    
    # # EC2 specific data extraction
    # attributes = pricing_data.get('product', {}).get('attributes', {})
    # instance_type = attributes.get('instanceType')
    # operating_system = attributes.get('operatingSystem')
    # cpu = attributes.get('vcpu')
    # memory = attributes.get('memory')
    # network_performance = attributes.get('networkPerformance')
    # tenancy = attributes.get('tenancy')

    # # Extract price and description
    # price_list = pricing_data.get('terms', {}).get('OnDemand', {})
    # for sku_details in price_list.values():
    #     for offer_term_code, offer_term_details in sku_details.get('priceDimensions', {}).items():
    #         description = offer_term_details.get('description')
    #         price_per_unit = offer_term_details.get('pricePerUnit', {}).get('USD')

    #         # Print extracted data to the console
    #         print(f"Compute ---------------------------------------------")
    #         print(f"SKU: {sku}")
    #         print(f"Instance Type: {instance_type}")
    #         print(f"Operating System: {operating_system}")
    #         print(f"CPU: {cpu}")
    #         print(f"Memory: {memory}")
    #         print(f"Network Performance: {network_performance}")
    #         print(f"Tenancy: {tenancy}")
    #         print(f"Description: {description}")
    #         print(f"Price per Unit: {price_per_unit}")
    #         print(f"Compute ---------------------------------------------")
    #         break
    #     break


def process_and_save_data(sku, service_code, pricing_data):
    # Check if SKU is part of AmazonEC2 and not "HY3BZPP2B6K8MSJF"
    if service_code == "AmazonEC2" and sku != "HY3BZPP2B6K8MSJF":
        process_ec2_data(sku, pricing_data)
    else:
        # Handle other cases or simply pass
        pass

    # Return the original pricing_data for the Django view
    return pricing_data
#     if service_code == "AmazonEC2":
#         if sku == "HY3BZPP2B6K8MSJF":
#             # Save to StorageSpecifications table
#             # ...
#         else:
#             # Save to ComputeSpecifications table
#             # ...

#     elif service_code == "AmazonDynamoDB":
#         # Save to DatabaseStorageVolume table
#         # ...

#     elif service_code == "AmazonS3" or service_code == "AmazonEFS":
#         # Save to StorageSpecifications table
#         # ...

#     elif service_code == "AmazonRDS" and sku == "QVD35TA7MPS92RBC":
#         # Save to DatabaseStorageVolume table
#         # ...














# --------------------------------------was working perfectlty for the specificd sku in the url-------------------------------------------------------------
# # Dictionary mapping SKU to Service Code
# sku_to_service_code = {
#     "3DG6WFZ5QW4JAAHJ": "AmazonEC2",  # 1 vCPU - 2 RAM (Standard)
#     "3K59PVQYWBTWXEHT": "AmazonEC2",  # 2 vCPU - 4 RAM (Standard)
#     "7WVK4XHSDKCTP5FX": "AmazonEC2",  # 1 vCPU - 2 RAM (Standard)
#     "4QB2537CEAFFV88T": "AmazonEC2",  # 2 vCPU - 4 RAM (Standard)
    
#     "F3E2EDSYC6ZNW7XP": "AmazonDynamoDB",  # $0.25/gb storage
#     "MV3A7KKN6HB749EA": "AmazonRDS",  #8 GiB memory singe AZ SQL Server
#     "QVD35TA7MPS92RBC": "AmazonRDS",   # SQL   Single-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month ServiceCode= AmazonRDS

#     "WP9ANXZGBYYSGJEA": "AmazonS3",  # $$0.022/GB monthly
#     "YFV3RHAD3CDDP3VE": "AmazonEFS",  #standard storage general purpose, $0.30 per GB-Mo
#     "HY3BZPP2B6K8MSJF": "AmazonEC2",   # gp2-general purpose storage 0.10 per GB-Mo

#     # Add other SKUs and their corresponding service codes here
# }

# def get_pricing(request):
#     sku = request.GET.get('sku')
#     if not sku:
#         return HttpResponse("SKU parameter is missing", status=400)

#     service_code = sku_to_service_code.get(sku)
#     if not service_code:
#         return HttpResponse(f"Service code not found for SKU {sku}", status=404)

#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode=service_code,
#         Filters=[{'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}],
#         MaxResults=1
#     )

#     if response['PriceList']:
#         pricing_data = json.loads(response['PriceList'][0])
#         return JsonResponse(pricing_data, safe=False, json_dumps_params={'indent': 4})
#     else:
#         return HttpResponse(f"No pricing data found for SKU {sku}", status=404)
#-----------------------------------------------------------------------------------------------------------------------------------------

# specify each sku and the serviceCode for it
# Call the api with sku and service code
# store/update to the tables with sku information (automate those three steps every morning)
# get submitted form and make backend logic for it
#
#
#







# def get_pricing(request):
#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode='AmazonEC2',
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}
#         ],
#         MaxResults=1
#     )

#     if response['PriceList']:
#         price_data = json.loads(response['PriceList'][0])
#         pricing_info = process_price_data(price_data)

#         provider, _ = Provider.objects.get_or_create(name='AWS')
#         cloud_service, _ = CloudService.objects.get_or_create(
#             provider=provider,
#             service_type='Compute',
#             defaults={'description': pricing_info['Description']}
#         )

#         ComputeSpecifications.objects.update_or_create(
#             sku=pricing_info['SKU'],  # Include SKU as a lookup field
#             defaults={
#             'cloud_service': cloud_service,
#             'instance_type': pricing_info['Instance Type'],
#             'operating_system': pricing_info['Operating System'],
#             'cpu': pricing_info['vCPU'],
#             'memory': pricing_info['Memory'],
#             'network_performance': pricing_info['Network Performance'],
#             'tenancy': pricing_info['Tenancy'],
#             'description': pricing_info['Description'],
#             'price_per_unit': pricing_info['Price per Unit'],
#             'currency': 'USD',  # Assuming currency is always USD
#             'updated_at': timezone.now(),  # Explicitly set the updated_at field

#             }
#         )
#         return HttpResponse(f"Updated or added new pricing and specifications for SKU {sku}: {pricing_info['Price per Unit']} with vCPU {pricing_info['vCPU']} and Memory {pricing_info['Memory']}", content_type='text/plain')
#     else:
#         return HttpResponse(f"No pricing information found for SKU {sku}", content_type='text/plain')

# def process_price_data(price_data):
#     product_attrs = price_data.get('product', {}).get('attributes', {})
#     sku = price_data.get('product', {}).get('sku')

#     on_demand_data = price_data.get('terms', {}).get('OnDemand', {})
#     for term_id, term_details in on_demand_data.items():
#         for price_dimension_key, price_dimension in term_details.get('priceDimensions', {}).items():
#             description = price_dimension.get('description')
#             price_per_unit = price_dimension.get('pricePerUnit', {}).get('USD')
            
#             return {
#                 "SKU": sku,
#                 "Instance Type": product_attrs.get('instanceType'),
#                 "Operating System": product_attrs.get('operatingSystem'),
#                 "vCPU": product_attrs.get('vcpu'),
#                 "Memory": product_attrs.get('memory'),
#                 "Physical Processor": product_attrs.get('physicalProcessor'),
#                 "Network Performance": product_attrs.get('networkPerformance'),
#                 "Tenancy": product_attrs.get('tenancy'),
#                 "Description": description,
#                 "Price per Unit": price_per_unit,
#                 "Unit": "Hrs"
#             }

#     return {}

# Note: there is an assumption that the presence of USD in pricePerUnit and that we always have OnDemand data in our response.
