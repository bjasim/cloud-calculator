
# -----------------------TO RUN IT---------------------------------------
# localhost/oracle/get-pricing/

#
#   BudgetCloud - Oracle Service Pricing/Details
#
from django.shortcuts import render
from django.http import HttpResponse
# from aws_app.models import Provider, CloudService, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications
import oci
import requests

# Create your views here.
def get_pricing(request):



    return HttpResponse("oracle App")

#Database code.
# ---
# ---
# ---

#Instance details.
def fetch_instance_details():
    compute_client = oci.core.ComputeClient(config)
    shapes = compute_client.list_shapes(compartment_id=config["tenancy"]).data

    for shape in shapes:
        print(f"Shape: {shape.shape}, CPUs: {shape.ocpus}, RAM: {shape.memory_in_gbs} GB")

#Storage [NOT WORKING].
def fetch_volume_details():
    block_storage_client = oci.core.BlockstorageClient(config)
    volumes = block_storage_client.list_volumes(compartment_id=config["tenancy"]).data

    for volume in volumes:
        print(f"Volume: {volume.display_name}, Size: {volume.size_in_gbs} GB, Availability Domain: {volume.availability_domain}")

#Database.
def fetch_database_options():
    database_client = oci.database.DatabaseClient(config)
    db_versions = database_client.list_db_versions(compartment_id=config["tenancy"]).data
    db_shapes = database_client.list_db_system_shapes(compartment_id=config["tenancy"]).data

    print("\nAvailable Database Versions:")
    for version in db_versions:
        print(f"Version: {version.version}")

    print("\nAvailable Database Shapes:")
    for shape in db_shapes:
        print(f"Shape: {shape.shape}")


#Networking [NOT WORKING].
def fetch_networking_options():
    virtual_network_client = oci.core.VirtualNetworkClient(config)
    vcns = virtual_network_client.list_vcns(compartment_id=config["tenancy"]).data

#Pricing.
def fetch_filtered_api_data():

    url = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        keywords = ["Compute - Virtual Machine", "Storage", "Database", "Networking"]  
        
        #Store products that have usd prices.
        products_with_usd = []

        for product in json_data['items']:
            service_category = product.get('serviceCategory', '')
            if any(keyword in service_category for keyword in keywords):
                usd_localizations = [localization for localization in product.get('currencyCodeLocalizations', [])
                                     if localization.get('currencyCode') == 'USD']
                
                usd_prices = [price for localization in usd_localizations for price in localization.get('prices', [])]
                
                if usd_prices:

                    #Calculate monthly cost.
                    for price in usd_prices:
                        price['monthlyCost'] = price.get('value', 0) * 744
                    
                    filtered_product = {
                        'partNumber': product.get('partNumber'),
                        'displayName': product.get('displayName'),
                        'metricName': product.get('metricName'),
                        'serviceCategory': service_category,
                        'usdPrices': usd_prices,
                        'sortKey': keywords.index(next((keyword for keyword in keywords if keyword in service_category), 'Other'))
                    }
                    products_with_usd.append(filtered_product)
        
        sorted_products = sorted(products_with_usd, key=lambda x: (x['sortKey'], x['serviceCategory']))

        for product in sorted_products:
            print(f"Part Number: {product['partNumber']}")
            print(f"Display Name: {product['displayName']}")
            print(f"Metric Name: {product['metricName']}")
            print(f"Service Category: {product['serviceCategory']}")
            print("USD Prices:")
            for price in product['usdPrices']:
                print(f"  - Model: {price['model']}")
                print(f"    Value per hour: ${price['value']}")
                print(f"    Estimated Monthly Cost (744 hours): ${price['monthlyCost']}")
            print("-----------------------------------")

    else:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")

#----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    config_file_path = "c:/Users/Philip/.oci/config"
    profile_name = "DEFAULT"

    config = oci.config.from_file(file_location=config_file_path, profile_name=profile_name)
    
    fetch_filtered_api_data()
    fetch_instance_details()
    fetch_volume_details()
    fetch_database_options()
    fetch_networking_options()
    
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
