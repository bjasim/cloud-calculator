

# import boto3
# import json
# from django.http import HttpResponse
# type = 't4g.medium'

# def testing(request):
#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode='AmazonEC2',
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': type},
#             # Additional filters can be added if the API supports them
#         ],
#         MaxResults=100
#     )
#     pricing_info = []

#     for price_str in response['PriceList']:
#         price_data = json.loads(price_str)
#         process_price_data(price_data, pricing_info)

#     return HttpResponse(json.dumps(pricing_info, indent=4), content_type='application/json')

# def process_price_data(price_data, pricing_info):
#     product_attrs = price_data.get('product', {}).get('attributes', {})
#     instance_type = product_attrs.get('instanceType')
#     operating_system = product_attrs.get('operatingSystem')
#     vcpu = product_attrs.get('vcpu')
#     memory = product_attrs.get('memory')
#     physical_processor = product_attrs.get('physicalProcessor')
#     network_performance = product_attrs.get('networkPerformance')
#     tenancy = product_attrs.get('tenancy')
#     sku = price_data.get('product', {}).get('sku')  # Extract the SKU

    

#     # Check if instance type is t2.small and operating system is Ubuntu
#     if instance_type == type and 'Ubuntu' in operating_system:
#         on_demand_data = price_data.get('terms', {}).get('OnDemand', {})
#         for term_id, term_details in on_demand_data.items():
#             for price_dimension_key, price_dimension in term_details.get('priceDimensions', {}).items():
#                 description = price_dimension.get('description')
#                 price_per_unit = price_dimension.get('pricePerUnit', {}).get('USD')
#                 unit = price_dimension.get('unit')

#                 pricing_info.append({
#                     "SKU": sku,  # Include the SKU in the output
#                     "Instance Type": instance_type,
#                     "Operating System": operating_system,
#                     "vCPU": vcpu,
#                     "Memory": memory,
#                     "Physical Processor": physical_processor,
#                     "Network Performance": network_performance,
#                     "Tenancy": tenancy,
#                     "Description": description,
#                     "Price per Unit": price_per_unit,
#                     "Unit": unit,
#                 })



import boto3
import json
from django.http import HttpResponse

def testing(request):
    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        # ServiceCode='AmazonDynamoDB',
        # ServiceCode='AmazonS3',
        # ServiceCode='AmazonEFS',
        # ServiceCode='AmazonEC2',  
        ServiceCode='AmazonBalancer',
        

        Filters=[
            # {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Storage'},
            # {'Type': 'TERM_MATCH', 'Field': 'volumeApiName', 'Value': 'gp2'},  # Example: Filter for General Purpose SSD (gp2)
            # {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'},  # Corresponds to 'us-east-1'

            # {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Storage instance'},
            # {'Type': 'TERM_MATCH', 'Field': 'volumeName', 'Value': 'gp2'},  # Filter for General Purpose SSD (gp2)
            # {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'ap-south-1'},
            # {'Type': 'TERM_MATCH', 'Field': 'databaseEdition', 'Value': 'standard'},
            # {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': 'SQL Server'},
            # {'Type': 'TERM_MATCH', 'Field': 'instanceFamily', 'Value': 'General Purpose'},
            # {'Type': 'TERM_MATCH', 'Field': 'instanceTypeFamily', 'Value': 'M4'},
            # Filter for On-Demand Read and Write Requests
            # {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'API Request'},
            # Filter for On-Demand Storage pricing
            # {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Database Storage'},
            # Filter for specific AWS region (e.g., 'us-east-1')
            # {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'},

            # {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Database Instance'},
            # {'Type': 'TERM_MATCH', 'Field': 'volumeName', 'Value': 'gp2'},  # Filter for General Purpose SSD (gp2)
            # {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': 'us-east-1'},
            # {'Type': 'TERM_MATCH', 'Field': 'databaseEdition', 'Value': 'standard'},
            # {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': 'DynamDB'},
            # {'Type': 'TERM_MATCH', 'Field': 'instanceFamily', 'Value': 'General Purpose'},
            # {'Type': 'TERM_MATCH', 'Field': 'instanceTypeFamily', 'Value': 'M4'}


        ],
        MaxResults=100
    )
    pricing_info = []

    for price_str in response['PriceList']:
        try:
            price_data = json.loads(price_str)
            pricing_info.append(price_data)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")

    return HttpResponse(json.dumps(pricing_info, indent=4), content_type='application/json')

# import boto3
# import json
# from django.http import HttpResponse

# def testing(request):
#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode='AmazonRDS',  # Change this to the appropriate service code for databases
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': 'NoSQL'},  # Filter for NoSQL databases
#             # Additional filters can be added if needed
#         ],
#         MaxResults=100
#     )
#     pricing_info = []

#     for price_str in response['PriceList']:
#         price_data = json.loads(price_str)
#         process_price_data(price_data, pricing_info)

#     return HttpResponse(json.dumps(pricing_info, indent=4), content_type='application/json')

# def process_price_data(price_data, pricing_info):
#     product_attrs = price_data.get('product', {}).get('attributes', {})
#     db_engine = product_attrs.get('databaseEngine')
#     deployment_option = product_attrs.get('deploymentOption')
#     instance_class = product_attrs.get('instanceClass')
#     sku = price_data.get('product', {}).get('sku')  # Extract the SKU

#     # Filter for NoSQL databases
#     if 'NoSQL' in db_engine:
#         on_demand_data = price_data.get('terms', {}).get('OnDemand', {})
#         for term_id, term_details in on_demand_data.items():
#             for price_dimension_key, price_dimension in term_details.get('priceDimensions', {}).items():
#                 description = price_dimension.get('description')
#                 price_per_unit = price_dimension.get('pricePerUnit', {}).get('USD')
#                 unit = price_dimension.get('unit')

#                 pricing_info.append({
#                     "SKU": sku,
#                     "Database Engine": db_engine,
#                     "Deployment Option": deployment_option,
#                     "Instance Class": instance_class,
#                     "Description": description,
#                     "Price per Unit": price_per_unit,
#                     "Unit": unit,
#                 })



# import boto3
# import json
# from django.http import HttpResponse

# def testing(request):
#     sku = "4QB2537CEAFFV88T"

#     client = boto3.client('pricing', region_name='us-east-1')
#     response = client.get_products(
#         ServiceCode='AmazonEC2',
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}
#         ],
#         MaxResults=100
#     )
#     pricing_info = []

#     for price_str in response['PriceList']:
#         price_data = json.loads(price_str)
#         process_price_data(price_data, pricing_info)

#     return HttpResponse(json.dumps(pricing_info, indent=4), content_type='application/json')

# def process_price_data(price_data, pricing_info):
#     # Include all the product details.
#     product_details = price_data.get('product', {})
#     attributes = product_details.get('attributes', {})
#     sku = product_details.get('sku')
    
#     # Include all the pricing details.
#     terms = price_data.get('terms', {})
#     on_demand_details = terms.get('OnDemand', {})
#     on_demand = {}
#     for term_id, term_detail in on_demand_details.items():
#         on_demand[term_id] = term_detail

#     # Append all details to pricing_info list.
#     pricing_info.append({
#         "SKU": sku,
#         "Product Details": product_details,
#         "Attributes": attributes,
#         "Terms": terms,
#         "On Demand": on_demand,
#     })

#     return pricing_info


