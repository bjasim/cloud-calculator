

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
    sku = "4QB2537CEAFFV88T"

    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}
        ],
        MaxResults=100
    )
    pricing_info = []

    for price_str in response['PriceList']:
        price_data = json.loads(price_str)
        process_price_data(price_data, pricing_info)

    return HttpResponse(json.dumps(pricing_info, indent=4), content_type='application/json')

def process_price_data(price_data, pricing_info):
    # Include all the product details.
    product_details = price_data.get('product', {})
    attributes = product_details.get('attributes', {})
    sku = product_details.get('sku')
    
    # Include all the pricing details.
    terms = price_data.get('terms', {})
    on_demand_details = terms.get('OnDemand', {})
    on_demand = {}
    for term_id, term_detail in on_demand_details.items():
        on_demand[term_id] = term_detail

    # Append all details to pricing_info list.
    pricing_info.append({
        "SKU": sku,
        "Product Details": product_details,
        "Attributes": attributes,
        "Terms": terms,
        "On Demand": on_demand,
    })

    return pricing_info


