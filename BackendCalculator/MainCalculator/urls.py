from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from azure_app.views import ViewHello
from azure_app.views import compute_fetch_view
from azure_app.views import storage_fetch_view
from azure_app.views import networking_fetch_view
from azure_app.views import database_fetch_view


router = DefaultRouter()
router.register("api/results", ViewHello, basename="ViewHello")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),
    # Azure catagories
    path('compute-fetch/', compute_fetch_view, name='fetch-compute'),
    path('storage-fetch/', storage_fetch_view, name='fetch-storage'),
    path('networking-fetch/', networking_fetch_view, name='fetch-networking'),
    path('database-fetch/', database_fetch_view, name='fetch-database'),
] + router.urls
