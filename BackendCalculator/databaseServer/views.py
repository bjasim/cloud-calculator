from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from azure_app.views import calculated_data_Azure
from aws_app.views import calculated_data_AWS
from aws_app.views import calculated_data_AWS_basic
from azure_app.views import calculated_data_Azure_basic


from oracle_app.views import calculated_data_Oracle
from oracle_app.views import calculated_data_Oracle

from oracle_app.views import calculated_data_Oracle
from google_app.views import calculated_data_gcp



@csrf_exempt
def handle_advanced_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        
        monthly_budget = form_data.get('monthlyBudget')
        expected_cpu = form_data.get('expectedRAM')
        database_service = form_data.get('databaseService')
        database_size = form_data.get('databaseSize') if form_data.get('databaseService') != "noDatabase" else None
        cloud_storage = form_data.get('cloudStorage')
        storage_size = form_data.get('storageSize') if form_data.get('cloudStorage') != "No Storage" else None
        dns_connection = form_data.get('dnsConnection')
        cdn_connection = form_data.get('cdnConnection')
        scalability = form_data.get('scalability')
        location = form_data.get('location')

        aws_data = calculated_data_AWS(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)

        azure_data = calculated_data_Azure(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        Oracle_data = calculated_data_Oracle(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        google_data = calculated_data_gcp(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)

        combined_data = {
            'Azure': azure_data,
            'AWS': aws_data,
            'Google': google_data,
            'Oracle': Oracle_data
        }

        print(combined_data)
        return JsonResponse(combined_data)

    else:
        return HttpResponseBadRequest("Unsupported request method")


@csrf_exempt
def handle_basic_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        monthly_budget = form_data.get('monthlyBudget')
        expected_cpu = form_data.get('computeComplexity') 
        database_service = form_data.get('databaseService')
        database_size = form_data.get('expectedUsers')
        cloud_storage = form_data.get('dataStorageType')
        storage_size = form_data.get('expectedUsers')
        dns_connection = form_data.get('dnsFeature')
        cdn_connection = form_data.get('cdnNetworking')
        scalability = form_data.get('scalability')
        location = form_data.get('region')

        aws_data = calculated_data_AWS_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        Oracle_data = calculated_data_Oracle(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        google_data = calculated_data_gcp(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)

        compute_complexity = form_data.get('computeComplexity')
        expected_users = form_data.get('expectedUsers')  
        data_storage_type = form_data.get('dataStorageType')
        database_service = form_data.get('databaseService')
        budget = form_data.get('monthlyBudget')
        dns_feature = form_data.get('dnsFeature')
        cdn_networking = form_data.get('cdnNetworking')
        region = form_data.get('region')

        azure_data = calculated_data_Azure_basic(compute_complexity, expected_users, data_storage_type, database_service, dns_feature, cdn_networking, region, budget)

        combined_data = {
            'Azure': azure_data,
            'AWS': aws_data,
            'Google': google_data,
            'Oracle': Oracle_data
        }

        print(combined_data)
        # Return computed data as JSON response
        return JsonResponse(combined_data)
    else:
        # Return error response if the request method is not POST
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})



