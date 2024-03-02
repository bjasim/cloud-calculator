#
#   BudgetCloud - Oracle Service Pricing/Details
#
from rest_framework import viewsets
import requests
from rest_framework.response import Response
from django.http import HttpResponse
from databaseServer.models import Provider, CloudService, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications
from django.shortcuts import render
import sqlite3
import os
from django.db import transaction
import logging

#---------------------Add this to enable LOGGING----------------------: 
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

#Configure logging
logger = logging.getLogger(__name__)

def main():

    #API url
    url = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            items = json_data['items']

            #Clear info
            CloudService.objects.all().delete()
            ComputeSpecifications.objects.all().delete()
            StorageSpecifications.objects.all().delete()
            DatabaseSpecifications.objects.all().delete()
            NetworkingSpecifications.objects.all().delete()

            #Transaction ensures atomicity of the database operations
            with transaction.atomic():
                for product in items:
                    
                    #Initialize usd_price as None
                    usd_price = None

                    #Iterate through currencyCodeLocalizations to find USD prices
                    for currencyLocalization in product.get('currencyCodeLocalizations', []):
                        if currencyLocalization['currencyCode'] == 'USD':

                            usd_price = next((price['value'] for price in currencyLocalization.get('prices', []) if price['model'] == 'PAY_AS_YOU_GO'), None)
                            
                            #Exit loop once USD price is found
                            break  
                    
                    if not usd_price:
                        logger.info(f"Skipping product due to missing USD price: {product.get('displayName')}")
                        
                        #Skip if no USD price found
                        continue 

                    #Filters
                    service_category = product.get('serviceCategory', '')
                    if any(service_category.startswith(prefix) for prefix in ["Database -", "Storage -", "Database with", "Networking -"]) or service_category in ["Compute - Virtual Machine", "Storage", "Database", "Networking"]:
                        provider, created = Provider.objects.get_or_create(name='Oracle')
                        if created:
                            logger.info(f"Created new provider: Oracle")

                        cloud_service, created = CloudService.objects.get_or_create(
                            service_type=service_category, 
                            provider=provider
                        )
                        if created:
                            logger.info(f"Created new cloud service: {service_category}")

                        #Compute data.
                        if "Compute" in service_category:
                            ComputeSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=product.get('partNumber'),
                                unit_price=usd_price,
                            )

                        #Storage data.
                        elif "Storage" in service_category:
                            StorageSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=product.get('partNumber'),
                                unit_price=usd_price,
                                unit_of_storage=product.get('metricName'),
                            )
                        #Networking data.
                        elif "Networking" in service_category:
                            NetworkingSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=product.get('partNumber'),
                                unit_price=usd_price,
                                unit_of_measure=product.get('metricName'),
                            )
                        #Database data.
                        elif "Database" in service_category:
                            DatabaseSpecifications.objects.create(
                                name=product.get('displayName'),
                                provider=provider,
                                cloud_service=cloud_service,
                                sku=product.get('partNumber'),
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

#View function that is mapped to the URL for triggering the data fetch.
def fetch_pricing_data(request):
    return main()



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