from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from azure_app.views import calculated_data_Azure, calculated_data_Azure_basic


@csrf_exempt
def handle_advanced_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        monthly_budget = form_data.get('monthlyBudget')
        expected_cpu = form_data.get('expectedRAM')  # Assuming the CPU field stores RAM information
        database_service = form_data.get('databaseService')
        database_size = form_data.get('databaseSize')
        cloud_storage = form_data.get('cloudStorage')
        storage_size = form_data.get('storageSize')
        dns_connection = form_data.get('dnsConnection')
        cdn_connection = form_data.get('cdnConnection')
        scalability = form_data.get('scalability')
        location = form_data.get('location')

        azure_data = calculated_data_Azure(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        aws_data = calculated_data_Azure(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        google_data = calculated_data_Azure(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        Oracle_data = calculated_data_Azure(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)

        combined_data = {
            'Azure': azure_data,
            'AWS': aws_data,
            'Google': google_data,
            'Oracle': Oracle_data
        }

        # print(calculated_data)
        # # Return computed data as JSON response
        # return JsonResponse(calculated_data)
        print(combined_data)
        # Return computed data as JSON response
        return JsonResponse(combined_data)

    else:
        # Return HTTP 400 Bad Request for unsupported request methods
        return HttpResponseBadRequest("Unsupported request method")


@csrf_exempt
def handle_basic_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        database_service_Azure = form_data.get('databaseService')
        expected_cpu_Azure = form_data.get('expectedRAM')  # Assuming the CPU field stores RAM information
        cloud_storage_Azure = form_data.get('cloudStorage')
        networking_feature_Azure = form_data.get('networkingFeature')

        azure_data = calculated_data_Azure_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        aws_data = calculated_data_Azure_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        google_data = calculated_data_Azure_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)
        Oracle_data = calculated_data_Azure_basic(monthly_budget, expected_cpu, database_service, database_size, cloud_storage, storage_size, dns_connection, cdn_connection, scalability, location)

        combined_data = {
            'Azure': azure_data,
            'AWS': aws_data,
            'Google': google_data,
            'Oracle': Oracle_data
        }

        # print(calculated_data)
        # # Return computed data as JSON response
        # return JsonResponse(calculated_data)
        print(combined_data)
        # Return computed data as JSON response
        return JsonResponse(combined_data)
    else:
        # Return error response if the request method is not POST
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})


