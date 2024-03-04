from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from azure_app.views import ViewHello
from azure_app.views import compute_fetch_view
from azure_app.views import storage_fetch_view
from azure_app.views import networking_fetch_view
from azure_app.views import database_fetch_view
from aws_app.views import get_pricing
from aws_app.views import aws_compute_fetch
from aws_app.views import aws_storage_fetch
from aws_app.views import aws_rds_fetch
from aws_app.views import aws_vpc_fetch
from aws_app.views import aws_route53_fetch
from aws_app.views import aws_direct_fetch
from aws_app.views import aws_cloudfront_fetch




from testing.views import testing
# from django.urls import include
from databaseServer.views import handle_advanced_form_submission
from databaseServer.views import handle_basic_form_submission


router = DefaultRouter()
router.register("api/results", ViewHello, basename="ViewHello")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),
    # handel submit advanced form
    path('api/submit-advanced-form/', handle_advanced_form_submission, name='submit_advanced_form'),
    # handel submit basic form
    path('api/submit-basic-form/', handle_basic_form_submission, name='submit_basic_form'),
    # Azure catagories
    path('compute-fetch/', compute_fetch_view, name='fetch-compute'),
    path('storage-fetch/', storage_fetch_view, name='fetch-storage'),
    path('networking-fetch/', networking_fetch_view, name='fetch-networking'),
    path('database-fetch/', database_fetch_view, name='fetch-database'),
    
    # AWS related--------------------------------------------------
    path('aws/', get_pricing, name='get-pricing'),   #fetch pricing details to database tables for all services
    path('aws-compute-fetch/', aws_compute_fetch, name='aws-compute-fetch'),    # Fetch to db for compute only
    path('aws-storage-fetch/', aws_storage_fetch, name='aws-storage-fetch'),    # Fetch to db for storage only
    path('aws-rds-fetch/', aws_rds_fetch, name='aws-rds-fetch'),                # Fetch to db for database services only
    path('aws-vpc-fetch/', aws_vpc_fetch, name='aws-vpc-fetch'),                # Fetch to db for VPC only
    path('aws-route53-fetch/', aws_route53_fetch, name='aws-route53-fetch'),    # Fetch to db for route53 only
    path('aws-direct-fetch/', aws_direct_fetch, name='aws-direct-fetch'),       # Fetch to db for direct connect only
    path('aws-cloudfront-fetch/', aws_cloudfront_fetch, name='aws-cloudfront-fetch'),    # Fetch to db for cloudfront only
    path('testing/', testing, name='testing'),                  # This is for testing purposes only and will be removed later
] + router.urls
