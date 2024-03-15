from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import json
from azure_app.views import calculated_data_Azure, calculated_data_Oracle


@csrf_exempt
def handle_advanced_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        database_service_Azure = form_data.get('databaseService')
        expected_cpu_Azure = form_data.get('expectedRAM')  # Assuming the CPU field stores RAM information
        cloud_storage_Azure = form_data.get('cloudStorage')
        networking_feature_Azure = form_data.get('networkingFeature')

        calculated_data = calculated_data_Azure(database_service_Azure, expected_cpu_Azure, cloud_storage_Azure, networking_feature_Azure)
        calculated_data1 = calculated_data_Oracle(database_service_Azure, expected_cpu_Azure, cloud_storage_Azure, networking_feature_Azure)

         # Merge the dictionaries
        merged_data = {**calculated_data, **calculated_data1}

        print(calculated_data)
        # Return computed data as JSON response
        return JsonResponse(calculated_data)
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

        calculated_data1 = calculated_data_Azure(database_service_Azure, expected_cpu_Azure, cloud_storage_Azure, networking_feature_Azure)

        print(calculated_data1)
        # Return computed data as JSON response
        return JsonResponse(calculated_data1)
    else:
        # Return error response if the request method is not POST
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})


