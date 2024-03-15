#
#   BudgetCloud - Oracle
#
from django.shortcuts import render
from rest_framework import viewsets
import requests
import logging
from rest_framework.response import Response
from django.http import HttpResponse
from django.db import transaction
from databaseServer.models import Provider, CloudService, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications, ComputeSpecifications

#Configure logging
logger = logging.getLogger(__name__)

#----------------Add this to: [MainCalculator -> Settings.py] to enable LOGGING----------------------: 
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'INFO',  # Set to 'DEBUG' to see all log messages
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         '': {  # This is the root logger
#             'handlers': ['console'],
#             'level': 'INFO',  # Adjust as needed; 'DEBUG' shows everything
#             'propagate': True,
#         },
#     },
# }

#Needed SKUs and their categories.
sku_to_category = {

    #cpu - E4 standard
    'B93113': 'compute',
    #ram - E4 standard
    'B93114': 'compute',
    #cpu - E5 standard
    'B97384': 'compute',
    #ram - E5 standard
    'B97385': 'compute',

    #Object
    'B91628': 'storage',
    #File
    'B89057': 'storage',
    #Block
    'B91961': 'storage',

    #DNS 1,000,000 Queries
    'B88525': 'networking',
    #North America, Europe, and UK Outbound per GB
    'B88327': 'networking',
    #APAC, Japan, and South America Outbound per GB
    'B93455': 'networking',
    #Middle East and Africa Outbound per GB
    'B93456': 'networking',
    #Load Balancer per hour
    'B96485': 'networking',

    #NoSQL
    'B89739': 'database',
    #PostgreSQL
    'B99062': 'database',
    #SQL
    'B92426': 'database',
}

#Specific Pricing data retrieved in JSON file from Oracle product Api.
def get_oracle_pricing(request):

    url = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            items = json_data['items']

            #Deletes ONLY oracle data.
            CloudService.objects.filter(provider__name="Oracle").delete()
            ComputeSpecifications.objects.filter(provider__name="Oracle").delete()
            StorageSpecifications.objects.filter(provider__name="Oracle").delete()
            DatabaseSpecifications.objects.filter(provider__name="Oracle").delete()
            NetworkingSpecifications.objects.filter(provider__name="Oracle").delete()

            with transaction.atomic():
                for product in items:
                    sku = product.get('partNumber')
                    service_category = sku_to_category.get(sku)

                    if service_category:
                        usd_price = None
                        for currencyLocalization in product.get('currencyCodeLocalizations', []):
                            if currencyLocalization['currencyCode'] == 'USD':

                                #Find all prices with the 'PAY_AS_YOU_GO' model
                                pay_as_you_go_prices = [price for price in currencyLocalization.get('prices', []) if price['model'] == 'PAY_AS_YOU_GO']
                                
                                #Initialize usd_price as None
                                usd_price = None

                                #Apply special logic only for part number B91628
                                if sku == "B91628":

                                    #Further filter to find a non-free tier for B91628
                                    usd_price = next((price['value'] for price in pay_as_you_go_prices if 'rangeMax' in price and price.get('value', 0) > 0 and price.get('rangeMax', 0) > 10), None)
                                else:
                                    #Default behavior for all other part numbers
                                    usd_price = next((price['value'] for price in pay_as_you_go_prices if price.get('value', 0) > 0), None)

                                if usd_price is not None:
                                    break
                        
                        if usd_price is None:
                            logger.info(f"Skipping product due to missing USD price: {product.get('displayName')}")
                            continue

                        provider, _ = Provider.objects.get_or_create(name='Oracle')
                        cloud_service, _ = CloudService.objects.get_or_create(service_type=service_category, provider=provider)

                        if service_category == 'compute':
                            ComputeSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=sku,
                                unit_price=usd_price,
                            )
                        elif service_category == 'storage':
                            StorageSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=sku,
                                unit_price=usd_price,
                                unit_of_storage=product.get('metricName'),
                            )
                        elif service_category == 'networking':
                            NetworkingSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=sku,
                                unit_price=usd_price,
                                unit_of_measure=product.get('metricName'),
                            )
                        elif service_category == 'database':
                            DatabaseSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=sku,
                                unit_price=usd_price,
                                unit_of_storage=product.get('metricName'),
                            )
                        logger.info(f"Inserted product into database: {product.get('displayName')}")

                return HttpResponse("Data fetched and stored successfully.")
        else:
            return HttpResponse(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data due to an error: {e}")
        return HttpResponse(f"Failed to fetch data due to an error: {e}", status=500)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)

#Handles form submission for Oracle.
def calculated_data_Oracle(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    computed_data = {'provider': 'Oracle',}

#ADVANCED FORM
#-------------
    #Question #1: Monthly Budget
    #Answer Options: 
    # 
    # budget prices
    # 
    #Oracle Options: 
    #
    # ???????????????????????????????????????????  
    #

    #Question #2: vCPU and RAM
    #--Answer Options--:
    #
    # 1vCPU-2RAM
    # 2vCPU-4RAM
    # 4vCPU-16RAM
    # 8vCPU-32RAM
    # 12vCPU-48RAM
    # 16vCPU-64RAM
    #
    #--Oracle Options--:
    #
    # sku:B93113 (1 ocpu) - sku:B93114 (1 ram)
    # multiply by # of ram/ocpu
    # 1oCPU-2RAM
    # 1oCPU-4RAM
    # 2oCPU-16RAM
    # 4oCPU-32RAM
    # 6oCPU-48RAM
    # 8oCPU-64RAM
    #
 

    # #IF SCALIABILITY IS SELECTED 
    # #Add auto scaling to name
    # #Add load balancer price: B96485 * 744 [MIGHT BE FREE]

    #Configuration for compute types.
    cpu_configurations = {
        "1vCPU": {"multiplier": 1, "ram_cost_multiplier": 2, "ram_cost_per_unit": 0.015, "name_override": "1oCPU(1vCPU)-2RAM"},
        "2vCPUs": {"multiplier": 1, "ram_cost_multiplier": 4, "ram_cost_per_unit": 0.015, "name_override": "1oCPU(2vCPU)-4RAM"},
        "4vCPUs": {"multiplier": 2, "ram_cost_multiplier": 16, "ram_cost_per_unit": 0.015, "name_override": "2oCPU(4vCPU)-16RAM"},
        "8vCPUs": {"multiplier": 4, "ram_cost_multiplier": 32, "ram_cost_per_unit": 0.015, "name_override": "4oCPU(8vCPU)-32RAM"},
        "12vCPUs": {"multiplier": 6, "ram_cost_multiplier": 48, "ram_cost_per_unit": 0.015, "name_override": "6oCPU(12vCPU)-48RAM"},
        "16vCPUs": {"multiplier": 8, "ram_cost_multiplier": 64, "ram_cost_per_unit": 0.015, "name_override": "8oCPU(16vCPU)-64RAM"},
    }

    #Calculate cpu.
    if expected_cpu in cpu_configurations:
        config = cpu_configurations[expected_cpu]

        #Initialize
        name_override = ""  

        #Check database size and select compute instance based off that.
        if database_size in ["small", "medium"]:
            compute_sku = "B93113"
            name_override = "AMD - Standard - E4 - "  
            ram_sku = "B93114"

        elif database_size == "large":
            compute_sku = "B97384"
            name_override = "AMD - Standard - E5 - "
            ram_sku = "B97385"


        #Fetch RAM pricing details using the selected RAM SKU.
        ram_service = ComputeSpecifications.objects.filter(sku=ram_sku).first()
        if ram_service:
            #Adjust ram_cost_per_unit based on the fetched RAM service details.
            config["ram_cost_per_unit"] = float(ram_service.unit_price)

        #Fetch compute service details from the database using compute_sku.
        compute_service = ComputeSpecifications.objects.filter(sku=compute_sku).first()

        if compute_service:

            #Calculate the unit price based on the configuration.
            compute_total_price = round(((float(compute_service.unit_price) * config["multiplier"]) * 744) + (config["ram_cost_per_unit"] * config["ram_cost_multiplier"] * 744))

            #Update computed_data with the fetched details.
            computed_data['compute'] = {
                'name': f"{name_override + config["name_override"]} - {location}",
                'sku': f"{compute_service.sku}CPU - {ram_sku}RAM",
                'unit_price': f"{compute_total_price} USD Monthly",
            }

#------------------------------------------------------------------------------------------------

    #Question #3: DB Type
    #--Answer Options--:
    #
    # NoSQL
    # PostgreSQL
    # SQL
    # noDB
    #
    #--Oracle Options--:
    #
    # NoSQL = B89739
    # PostgreSQL = B99062
    # SQL = B92426
    # " "
    #
    #Check for the "No Storage" option first.
    if database_service == "noDatabase":
        computed_data['database'] = {
            'name': "No Database",
            'unit_price': "N/A",
            'unit_of_storage': None,
            'sku': "N/A",
            'provider': None,
            'cloud_service': None
        }
    else:
        #Map cloud storage types to their corresponding SKU.
        sku_mapping = {
            "noSQL": "B89739",
            "postgreSQL": "B99062",
            "sql": "B92426",
        }

        #Get the SKU for the current cloud_storage type.
        sku = sku_mapping.get(database_service)

        #Proceed only if a matching SKU was found.
        if sku:

            #Query for the storage instance based on the part number.
            database_instance = DatabaseSpecifications.objects.filter(sku=sku).first()
            if database_instance:

                #Change names
                if sku == "B89739":
                    name_override = "Oracle NoSQL"
                elif sku == "B99062":
                    name_override = "DB with PostgreSQL"
                elif sku == "B92426":
                    name_override = "Oracle MySQL"
                else:
                    name_override = database_instance.name

                #DB Size
                if database_size == "small":
                    db_size = 10
                elif database_size == "medium":
                    db_size = 100
                elif database_size == "large":
                    db_size = 1000

                database_total_price = round(float(database_instance.unit_price) * db_size)

                computed_data['database'] = {
                    'name': f"{name_override} - {db_size}GB - {location}",
                    'unit_price': f"{database_total_price} USD Monthly",
                    'unit_of_storage': database_instance.unit_of_storage,
                    'sku': database_instance.sku,
                    'provider': database_instance.provider.name,
                    'cloud_service': database_instance.cloud_service.service_type
                }

    #Question #4: DB Size
    #--Answer Options--:
    #
    # small 
    # med
    # large
    # v large
    # unsure
    #
    #--Oracle Options--:
    #
    # Multiply Q3 by this answer
    # 

    #Question #5: Cloud Storage
    #--Answer Options--:
    #
    # Object
    # File
    # Block
    # 
    #--Oracle Options--:
    # 
    # Object: B91628
    # File: B89057
    # Block: B91961
    # 
    #Check for the "No Storage" option first
    if cloud_storage == "No Storage":
        computed_data['storage'] = {
            'name': "No Storage",
            'unit_price': "N/A",
            'unit_of_storage': None,
            'sku': "N/A",
            'provider': None,
            'cloud_service': None
        }
    else:
        #Map cloud storage types to their corresponding SKU
        sku_mapping = {
            "Object Storage": "B91628",
            "Block Storage": "B91961",
            "File Storage": "B89057",
        }

        #Get the SKU for the current cloud_storage type
        sku = sku_mapping.get(cloud_storage)

        #Proceed only if a matching SKU was found
        if sku:
            #Query for the storage instance based on the part number
            storage_instance = StorageSpecifications.objects.filter(sku=sku).first()
            if storage_instance:

                #Change names.
                if sku == "B91628":
                    name_override = "Object Storage"
                elif sku == "B89057":
                    name_override = "File Storage"
                elif sku == "B91961":
                    name_override = "Block Storage"
                else:
                    name_override = storage_instance.name

                #Storage Size.
                if database_size == "small":
                    st_size = 1000
                    st_name = "1TB"
                elif database_size == "medium":
                    st_size = 10000
                    st_name = "10TB"
                elif database_size == "large":
                    st_size = 100000
                    st_name = "100TB"

                storage_total_price = round(float(storage_instance.unit_price) * st_size)

                #Display to frontend.
                computed_data['storage'] = {
                    'name': f"{name_override} - {st_name} - {location}",
                    'unit_price': f"{storage_total_price} USD Monthly",
                    'unit_of_storage': storage_instance.unit_of_storage,
                    'sku': storage_instance.sku,
                    'provider': storage_instance.provider.name,
                    'cloud_service': storage_instance.cloud_service.service_type
                }

    #Question #6: Storage Size
    #--Answer Options--:
    #
    # small
    # med
    # large
    # v large
    #
    #--Oracle Options--:
    #
    # Multiply Q5 by this answer
    #

    #Question #7 & #8: DNS and CDN
    #--Answer Options--:
    #
    # Yes or no
    #
    #--Oracle Options--:
    #
    # DNS = SKU: B88525 (say per 1,000,000 queries)
    #
    # CDN = Inbound: Free, Outbound: < 10 TB free (> 10tb depends on region)
    #
                

#ADD OUT BOUND CDN PER GB DATA DEPENDING ON LOCATION SELECTED BY USER
#
#   North America, Europe, and UK = B88327
#   APAC, Japan, and South America = B93455
#   Middle East and Africa = B93456
#

    #-----------------------CDN-------------------------            
    computed_data['networking'] = {
        'name': "", 
        'SKU': "", 
        'unit_price': "", 
        
    }
    #Check if the CDN option is enabled by the user.
    if cdn_connection == "Yes":
        computed_data['networking'] = {
            'name': "CDN",  
            'sku': "Varnish-Enterprise-6 for OCI",
            'unit_price': "OCI Marketplace",  
            }
        
    #---------------------DNS--------------------------    
    if dns_connection == "Yes":

        #Fetch DNS service details from the database.
        dns_service = NetworkingSpecifications.objects.first()
        
        if dns_service:
            
            #Update the DNS section within the networking part of computed_data with the fetched details.
            computed_data['networking'] = {
                'name': "DNS",
                'sku': dns_service.sku,
                'unit_price': f"| {dns_service.unit_price} USD Per 1,000,000 queries"
            }          

    #-----------------IF DNS AND CDN SELECTED---------------------------------------
    if dns_connection == "Yes" and cdn_connection == "Yes":

        #Fetch DNS service details from the database.
        dns_service = NetworkingSpecifications.objects.first()
        
        if dns_service:

            #Update the DNS section within the networking part of computed_data with the fetched details.
            computed_data['networking'] = {
                'name': "CDN & DNS",
                'sku': f" DNS:{dns_service.sku} CDN: Varnish-Enterprise-6",
                'unit_price': f"| DNS = {dns_service.unit_price} USD Per 1,000,000 queries | CDN = OCI Marketplace |" 
            }          

    
    #Question #9:
    #--Answer Options--:
    # 
    # Important or not important
    #
    #--Oracle Options--:
    #
    # Include or not include auto scaling [ADD TO COMPUTE NAME]
    #

    #Question #10:
    #--Answer Options--:
    #
    # Various Regions
    #
    #--Oracle Options--:
    #   
    # Answer: Enter region but NO difference in price
    #
    
    

#BASIC FORM
#----------
    #Question #1: Compute complexity
    #--Answer Options--:
    #
    # basic 2vcpu-4ram
    # moderate 8vcpu-32ram
    # intensive 16vcpu-64ram
    #
    #--Oracle Options--:
    # 
    # sku:B93113 (1 ocpu) - sku:B93114 (1 ram)
    # multiply by # of ram/ocpu
    # 
    # Basic: 1ocpu-4ram
    # Moderate: 4ocpu-32ram
    # Intensive: 8ocpu-64ram
    # 

    #Question #2: Expected Users
    #--Answer Options--:
    # 
    # <1000 = 50gb db storage
    # 5000 = 200gb
    # 10000+ = 1TB (add auto scaling to compute name)
    #            
    #--Oracle Options--:
    #
    # multiply DB size by this
    # 
                            
    #Question #3: Type of data
    #--Answer Options--:
    #   
    # files
    # database
    # multimedia
    #
    #--Oracle Options--:
    #   
    # File: B89057
    # Block: B91961
    # Object: B96625
    #

    #Question #4:
    #--Answer Options--:
    #
    #
    #
    #--Oracle Options--:
    #
    #
    #

    #Question #5:
    #--Answer Options--:
    #
    #
    #
    #--Oracle Options--:
    #
    #
    #
                
    #Question #6:
    #--Answer Options--: DNS
    #
    # "Yes" or "No"
    #
    #--Oracle Options--:
    #
    # 
    #

    #Question #7:
    #--Answer Options--: CDN
    #
    # "Yes" or "No"
    #
    #--Oracle Options--:
    #
    #
    #

    #Question #8:
    #--Answer Options--:
    #
    # Various Regions
    #
    #--Oracle Options--:
    #
    # Enter region but NO difference in price
    #

    plan_monthly_price = compute_total_price + storage_total_price + database_total_price

    plan_annual_price = round(float(plan_monthly_price) * 12)
    print("Total Monthly Plan Cost: ", plan_monthly_price)
    print("Total Monthly Plan Cost: ", plan_annual_price)

    computed_data['monthly'] = plan_monthly_price
    computed_data['annual'] = plan_annual_price

    return computed_data