from django.shortcuts import render
from django.http import HttpResponse
from aws_app.models import Provider, CloudService, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications
# -----------------------TO RUN IT---------------------------------------
# localhost/oracle/get-pricing/

# Create your views here.
def get_pricing(request):
    return HttpResponse("oracle App")
