from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import json
from azure_app.views import calculated_data_Azure
from aws_app.views import calculated_data_AWS


@csrf_exempt
def handle_advanced_form_submission(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print("Received form data:", form_data)
        database_service_Azure = form_data.get('databaseService')
        expected_cpu_Azure = form_data.get('expectedRAM')  # Assuming the CPU field stores RAM information
        cloud_storage_Azure = form_data.get('cloudStorage')
        networking_feature_Azure = form_data.get('networkingFeature')
        database_size_Azure = form_data.get('databaseSize')

        # calculated_data = calculated_data_Azure(database_service_Azure, expected_cpu_Azure, cloud_storage_Azure, networking_feature_Azure)
        calculated_data = calculated_data_AWS(database_service_Azure, database_size_Azure, expected_cpu_Azure, cloud_storage_Azure, networking_feature_Azure)

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

        # Print form data to console
        print("Received form data:", form_data)

        # Return success response
        return JsonResponse({'success': True})
    else:
        # Return error response if the request method is not POST
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})


