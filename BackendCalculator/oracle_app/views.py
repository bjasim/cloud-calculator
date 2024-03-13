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
    'B96625': 'storage',
    #File
    'B89057': 'storage',
    #Block
    'B91961': 'storage',

    #DNS 1,000,000 Queries
    'B88525': 'networking',

    #NoSQL
    'B89739': 'database',
    #PostgreSQL
    'B99062': 'database',
    #SQL
    'B92426': 'database',
}

def get_oracle_pricing(request):
    url = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            items = json_data['items']

            # Deletes ONLY oracle data.
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
                                usd_price = next((price['value'] for price in currencyLocalization.get('prices', []) if price['model'] == 'PAY_AS_YOU_GO'), None)
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

# Create your views here.
def calculated_data_Oracle(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location):
    computed_data = {'provider': 'Oracle',}  

#ADVANCED FORM
#-------------
    #Question #1: Monthly Budget
    #Answer Options: budget prices
    #Oracle Options: check price is under/over budget

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

#-------------------------------------------------------------------------------------
    # # SKUs for OCPU and RAM
    # cpu_sku = "B93113"
    # ram_sku = "B93114"

    # # Initial multipliers for CPUs and RAMs based on expected configurations
    # cpu_ram_configurations = {
    #     "1vCPU": {"cpu_multiplier": 0, "ram_multiplier": 2},
    #     "2vCPUs": {"cpu_multiplier": 0, "ram_multiplier": 4},
    #     "4vCPUs": {"cpu_multiplier": 2, "ram_multiplier": 16},
    #     "8vCPUs": {"cpu_multiplier": 4, "ram_multiplier": 32},
    #     "12vCPUs": {"cpu_multiplier": 6, "ram_multiplier": 48},
    #     "16vCPUs": {"cpu_multiplier": 8, "ram_multiplier": 64},
    # }

    # # Retrieve multipliers
    # multipliers = cpu_ram_configurations.get(expected_cpu, None)
    # if multipliers is None:
    #     return None  # or handle error as appropriate

    # # Assuming ComputeSpecifications and sku_mapping are defined
    # # Retrieve the unit prices for CPU and RAM
    # cpu_price = ComputeSpecifications.objects.filter(sku=cpu_sku).first().unit_price if multipliers["cpu_multiplier"] > 0 else 0
    # ram_price = ComputeSpecifications.objects.filter(sku=ram_sku).first().unit_price

    # # Calculate total cost
    # total_cost = (cpu_price * multipliers["cpu_multiplier"]) + (ram_price * multipliers["ram_multiplier"])
#------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------
    ##COMPUTE
    # sku = sku_mapping.get(expected_cpu)

    # # Proceed only if a matching SKU was found
    # if sku:
    #     # Query for the storage instance based on the part number
    #     compute_instance = ComputeSpecifications.objects.filter(sku=sku).first()
    #     if compute_instance:

            ##Multiply RAM and OCPU values 
    #         if expected_cpu:
                # if expected_cpu == "1vCPU":
                #     #[RAM] (B93114) * 2
                    
                # elif expected_cpu == "2vCPUs":
                #     #[RAM] (B93114) * 4

                # elif expected_cpu == "4vCPUs":
                #     #[RAM] (B93114) * 16
                #     #[OCPU] (B93113) * 2
                    
                # elif expected_cpu == "8vCPUs":
                #     #[RAM] (B93114) * 32
                #     #[OCPU] (B93113) * 4
                    
                # elif expected_cpu == "12vCPUs":
                #     #[RAM] (B93114) * 48
                #     #[OCPU] (B93113) * 6

                # elif expected_cpu == "16vCPUs":
                #     #[RAM] (B93114) * 64
                #     #[OCPU] (B93113) * 8
                    
            # compute_instance = ComputeSpecifications.objects.get(sku=compute_sku, provider__name='Oracle')
            # # unit_price = float(compute_instance.unit_price) * 720 # Convert unit price to float
            # compute_unit_price = float(compute_instance.unit_price)# Convert unit price to float

            # computed_data['compute'] = {
            #     'name': compute_instance.name,
            #     'unit_price': compute_unit_price,
            #     'cpu': compute_instance.cpu,
            #     'memory': compute_instance.memory,
            #     'sku': compute_instance.sku,
            #     'provider': compute_instance.provider.name,
            #     'cloud_service': compute_instance.cloud_service.service_type,
            #     'description': compute_instance.description  # Assuming there's a description field
            # }        
#---------------------------------------------------------------------------------------------------- 

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
    # Check for the "No Storage" option first
    if database_service == "noDatabase":
        computed_data['database'] = {
            'name': "No Database",  # Set name to "No Storage"
            # Set other fields to None or appropriate defaults
            'unit_price': "N/A",
            'unit_of_storage': None,
            'sku': "N/A",
            'provider': None,
            'cloud_service': None
        }
    else:
        # Map cloud storage types to their corresponding SKU
        sku_mapping = {
            "noSQL": "B89739",
            "postgreSQL": "B99062",
            "sql": "B92426",
        }

        # Get the SKU for the current cloud_storage type
        sku = sku_mapping.get(database_service)

        # Proceed only if a matching SKU was found
        if sku:
            # Query for the storage instance based on the part number
            database_instance = DatabaseSpecifications.objects.filter(sku=sku).first()
            if database_instance:

                #change names
                if sku == "B89739":
                    name_override = "Oracle NoSQL"
                elif sku == "B99062":
                    name_override = "DB with PostgreSQL"
                elif sku == "B92426":
                    name_override = "Oracle MySQL"
                else:
                    name_override = database_instance.name

                computed_data['database'] = {
                    'name': name_override,
                    'unit_price': database_instance.unit_price,
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
    # Object: B96625
    # File: B89057
    # Block: B91961
    # 
        # Check for the "No Storage" option first
    if cloud_storage == "No Storage":
        computed_data['storage'] = {
            'name': "No Storage",  # Set name to "No Storage"
            # Set other fields to None or appropriate defaults
            'unit_price': "N/A",
            'unit_of_storage': None,
            'sku': "N/A",
            'provider': None,
            'cloud_service': None
        }
    else:
        # Map cloud storage types to their corresponding SKU
        sku_mapping = {
            "Object Storage": "B96625",
            "Block Storage": "B91961",
            "File Storage": "B89057",
        }

        # Get the SKU for the current cloud_storage type
        sku = sku_mapping.get(cloud_storage)

        # Proceed only if a matching SKU was found
        if sku:
            # Query for the storage instance based on the part number
            storage_instance = StorageSpecifications.objects.filter(sku=sku).first()
            if storage_instance:

                #Change names
                if sku == "B96625":
                    name_override = "Object Storage"
                elif sku == "B89057":
                    name_override = "File Storage"
                elif sku == "B91961":
                    name_override = "Block Storage"
                else:
                    name_override = storage_instance.name

                computed_data['storage'] = {
                    'name': name_override,
                    'unit_price': storage_instance.unit_price,
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

    #Question #7: DNS
    #--Answer Options--:
    #
    # Yes or no
    #
    #--Oracle Options--:
    #
    # SKU: B88525 (say per 1,000,000 queries)
    #

    #Question #8: CDN
    #--Answer Options--:
    #
    # Yes or no
    #
    #--Oracle Options--:
    #
    # Inbound: Free
    # Outbound: < 10 TB free 
    #

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
    #--Answer Options--:
    #
    #
    #
    #--Oracle Options--:
    #
    #
    #

    #Question #7:
    #--Answer Options--:
    #
    #
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


    # if cloud_storage == "Object Storage":
    #     # Query for the storage instance based on the part number "B96625"
    #     storage_instance = StorageSpecifications.objects.filter(sku='B96625').first()
    #     if storage_instance:
    #         computed_data['storage'] = {
    #             'name': storage_instance.name,
    #             'unit_price': storage_instance.unit_price,
    #             'unit_of_storage': storage_instance.unit_of_storage,
    #             'sku': storage_instance.sku,  # This will be "B96625" for your specific query
    #             'provider': storage_instance.provider.name,
    #             'cloud_service': storage_instance.cloud_service.service_type
    #         }

    # plan_monthly_price = compute_total_price + storage_unit_price + total_db_price
    # # plan_monthly_price = compute_total_price + storage_unit_price

    # plan_annual_price = float(plan_monthly_price) * 12
    # print("Total Monthly Plan Cost: ", plan_monthly_price)
    # print("Total Annual Plan Cost: ", plan_annual_price)

    # computed_data['monthly'] = plan_monthly_price
    # computed_data['annual'] = plan_annual_price

    return computed_data

# ======================== Third Party Components ========================
# certifi
# * Copyright 2022, Kenneth Reitz
# * License: Mozilla Public License 2.0 (MPL 2.0)
# * Source code: https://github.com/certifi/python-certifi
# * Project home: https://certifi.io

# cryptography
# * Copyright (c) Individual contributors.
# * License: Apache License, BSD License, PSF License
# * Source code: https://github.com/pyca/cryptography
# * Project home: https://github.com/pyca/cryptography

# pyOpenSSL
# * Copyright 2001 The pyOpenSSL developers
# * License: Apache License 2.0
# * Source code: https://github.com/pyca/pyopenssl
# * Project home: https://www.pyopenssl.org/

# python-dateutil
# * Copyright 2017- Paul Ganssle <paul@ganssle.io> 2017- dateutil contributors (see AUTHORS file)
# * License: Apache License 2.0
# * Source code: https://github.com/dateutil/dateutil
# * Project home: https://dateutil.readthedocs.io/

# pytz
# * Copyright (c) 2003-2019 Stuart Bishop <stuart@stuartbishop.net>
# * License: The MIT License (MIT)
# * Source code: https://github.com/stub42/pytz
# * Project home: https://pythonhosted.org/pytz

# six
# * Copyright (c) 2010-2020 Benjamin Peterson
# * License: The MIT License (MIT)
# * Source code: https://github.com/benjaminp/six
# * Project home: https://github.com/benjaminp/six

# vendorize
# * Copyright (c) 2015, Michael Williamson All rights reserved
# * License: BSD 2-Clause "Simplified" License
# * Source code: https://github.com/mwilliamson/python-vendorize
# * Project home: https://github.com/mwilliamson/python-vendorize

# chardet
# * Copyright 2015, Mark Pilgrim, Dan Blanchard, Ian Cordasco
# * License: GNU Lesser General Public License v2.1
# * Source code: https://github.com/chardet/chardet
# * Project home: https://github.com/chardet/chardet

# httpsig_cffi
# * Copyright (c) 2014 Adam Knight 2012 Adam T. Lindsay (original author)
# * License: The MIT License (MIT)
# * Source code: https://github.com/hawkowl/httpsig_cffi
# * Project home: https://github.com/hawkowl/httpsig_cffi

# idna
# * Copyright (c) 2013-2021, Kim Davies All rights reserved
# * License: BSD 3-Clause "New" or "Revised" License
# * Source code: https://github.com/kjd/idna
# * Project home: https://github.com/kjd/idna

# jwt
# * Copyright 2017 Gehirn Inc
# * License: Apache License 2.0
# * Source code: https://github.com/GehirnInc/python-jwt
# * Project home: https://github.com/GehirnInc/python-jwt

# requests
# * Copyright 2019 Kenneth Reitz
# * License: Apache License 2.0
# * Source code: https://github.com/psf/requests
# * Project home: https://requests.readthedocs.io

# urllib3
# * Copyright (c) 2008-2020 Andrey Petrov and contributors (see CONTRIBUTORS.txt)
# * License: MIT License
# * Source code: https://github.com/urllib3/urllib3
# * Project home: https://urllib3.readthedocs.io

# circuitbreaker
# * Copyright (c) 2016-2020, Fabian Fuelling opensource@fabfuel.de. All rights reserved.
# * License: MIT License
# * Source code: https://github.com/fabfuel/circuitbreaker
# * Project home: https://pypi.org/project/circuitbreaker

# pycparser
# * Copyright (c) 2008-2020, Eli Bendersky All rights reserved.
# * License: BSD-3-Clause New License
# * Source code: https://github.com/eliben/pycparser
# * Project home: https://pypi.org/project/pycparser

# cffi
# * Copyright (C) 2005-2007, James Bielman  <jamesjb@jamesjb.com>
# * License: The MIT License
# * Source code: https://pypi.org/project/cffi/#files
# * Project home: https://cffi.readthedocs.io/en/latest

# sseclient
# * Copyright 2024 Maxime Petazzoni maxime.petazzoni@bulix.org
# * License: Apache License 2.0
# * Source code: https://github.com/mpetazzoni/sseclient
# * Project home: https://github.com/mpetazzoni/sseclient

# =============================== Licenses ===============================

# ------------------------------ MIT License -----------------------------

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ------------------------------------------------------------------------