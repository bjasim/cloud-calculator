# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
import requests
from rest_framework.response import Response
from django.http import HttpResponse
from databaseServer.models import Provider, CloudService, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications, ComputeSpecifications

# Create your views here.
def calculated_data_Oracle(database_service, expected_cpu, cloud_storage, networking_feature):
    computed_data = {'provider': 'Oracle',}  # Initialize dictionary to store computed data

    # Retrieve data from the database based on the provided keyword
    # if expected_cpu:
    #     # Query for the first compute instance
    #     compute_instance = ComputeSpecifications.objects.filter(cpu=expected_cpu).first()
    #     if compute_instance:
    #         computed_data['compute'] = {
    #             'name': compute_instance.name,
    #             'unit_price': compute_instance.unit_price,
    #             'cpu': compute_instance.cpu,
    #             'memory': compute_instance.memory,
    #             'sku': compute_instance.sku,
    #             'provider': compute_instance.provider.name,
    #             'cloud_service': compute_instance.cloud_service.service_type
    #         }

    if cloud_storage:
        # Query for the first storage instance based on the keyword "File"
        storage_instance = StorageSpecifications.objects.filter(name__icontains='File').first()
        if storage_instance:
            computed_data['storage'] = {
                'name': storage_instance.name,
                'unit_price': storage_instance.unit_price,
                'unit_of_storage': storage_instance.unit_of_storage,
                'sku': storage_instance.sku,
                'provider': storage_instance.provider.name,
                'cloud_service': storage_instance.cloud_service.service_type
            }

    if database_service:
        # Query for the first database instance
        database_instance = DatabaseSpecifications.objects.filter(name__icontains=database_service).first()
        if database_instance:
            computed_data['database'] = {
                'name': database_instance.name,
                'unit_price': database_instance.unit_price,
                'unit_of_storage': database_instance.unit_of_storage,
                'sku': database_instance.sku,
                'data_type': database_instance.data_type,
                'provider': database_instance.provider.name,
                'cloud_service': database_instance.cloud_service.service_type
            }
        else:
            computed_data['database'] = None

    if networking_feature:
        if 'Content' in networking_feature:
            # Query for the first networking instance based on the keyword "CDN"
            networking_instance = NetworkingSpecifications.objects.filter(name__icontains='CDN').first()
        else:
            # Query for the first networking instance based on the first word
            first_word = networking_feature.split()[0]
            networking_instance = NetworkingSpecifications.objects.filter(name__icontains=first_word).first()

        if networking_instance:
            computed_data['networking'] = {
                'name': networking_instance.name,
                'unit_price': networking_instance.unit_price,
                'unit_of_measure': networking_instance.unit_of_measure,
                'sku': networking_instance.sku,
                'provider': networking_instance.provider.name,
                'cloud_service': networking_instance.cloud_service.service_type
            }

    return computed_data