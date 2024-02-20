
import boto3
import json
from django.http import HttpResponse
from django.utils import timezone

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
# sku = "3DG6WFZ5QW4JAAHJ" # 1 vCPU  - 2 RAM ( Standard) 
# sku = "3K59PVQYWBTWXEHT" #2 vCPU  - 4 RAM ( Standard)
# sku = "7WVK4XHSDKCTP5FX" #4 vCPU  - 16 RAM ( Standard)  
sku = "4QB2537CEAFFV88T" #8 vCPU  - 32 RAM ( Standard) 

#-----------------------------------------------------------------------------
# 3.	Database Type:
# Question: "What type of database services are you looking for?"Relational (SQL)
# NoSQL
# SQL
# No database is required
#*****************************************************************************
# NoSQL 
# Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month
# Instance sku = "MV3A7KKN6HB749EA or PHXMADZ7H8JN3RRW" 8 GiB memory singe AZ or Multi-AZ
# No database is required

#----------------------------------If SQL is selected in the previous question---------------------------
# Question: "What is the expected size of your database?"
# Small (under 500 GB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month
# Medium (1 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month
# Large (2 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month
# Very large (5 TB) # Storage sku = "QVD35TA7MPS92RBC or YUPCZAH7K635UM3H" # SQL   Single-AZ or Multi-AZ )multiply with the size of the database ex. 100gb = 0.12-gb/month * 100GB = $12 a month
#*****************************************************************************
#----------------------------------If NoSQL is selected in the previous question---------------------------
# Question: "What is the expected size of your database?"
# Small (under 500 GB)
# Medium (1 TB)
# Large (2 TB)
# Very large (5 TB)
#*****************************************************************************




def get_pricing(request):


    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'sku', 'Value': sku}
        ],
        MaxResults=1
    )

    if response['PriceList']:
        price_data = json.loads(response['PriceList'][0])
        pricing_info = process_price_data(price_data)

        provider, _ = Provider.objects.get_or_create(name='AWS')
        cloud_service, _ = CloudService.objects.get_or_create(
            provider=provider,
            service_type='Compute',
            defaults={'description': pricing_info['Description']}
        )


        ComputeSpecifications.objects.update_or_create(
            sku=pricing_info['SKU'],  # Include SKU as a lookup field
            defaults={
            'cloud_service': cloud_service,
            'instance_type': pricing_info['Instance Type'],
            'operating_system': pricing_info['Operating System'],
            'cpu': pricing_info['vCPU'],
            'memory': pricing_info['Memory'],
            'network_performance': pricing_info['Network Performance'],
            'tenancy': pricing_info['Tenancy'],
            'description': pricing_info['Description'],
            'price_per_unit': pricing_info['Price per Unit'],
            'currency': 'USD',  # Assuming currency is always USD
            'updated_at': timezone.now(),  # Explicitly set the updated_at field

            }
        )

        return HttpResponse(f"Updated or added new pricing and specifications for SKU {sku}: {pricing_info['Price per Unit']} with vCPU {pricing_info['vCPU']} and Memory {pricing_info['Memory']}", content_type='text/plain')
    else:
        return HttpResponse(f"No pricing information found for SKU {sku}", content_type='text/plain')


def process_price_data(price_data):
    product_attrs = price_data.get('product', {}).get('attributes', {})
    sku = price_data.get('product', {}).get('sku')

    on_demand_data = price_data.get('terms', {}).get('OnDemand', {})
    for term_id, term_details in on_demand_data.items():
        for price_dimension_key, price_dimension in term_details.get('priceDimensions', {}).items():
            description = price_dimension.get('description')
            price_per_unit = price_dimension.get('pricePerUnit', {}).get('USD')
            
            return {
                "SKU": sku,
                "Instance Type": product_attrs.get('instanceType'),
                "Operating System": product_attrs.get('operatingSystem'),
                "vCPU": product_attrs.get('vcpu'),
                "Memory": product_attrs.get('memory'),
                "Physical Processor": product_attrs.get('physicalProcessor'),
                "Network Performance": product_attrs.get('networkPerformance'),
                "Tenancy": product_attrs.get('tenancy'),
                "Description": description,
                "Price per Unit": price_per_unit,
                "Unit": "Hrs"
            }

    return {}

# Note: there is an assumption that the presence of USD in pricePerUnit and that we always have OnDemand data in our response.
