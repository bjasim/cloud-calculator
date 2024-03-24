from django.contrib import admin
from .models import Provider, CloudService, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications

# Register your models here.
admin.site.register(Provider)
class CloudServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'provider')  # Specify the fields you want to display in the admin list view

# Register the CloudService model with the custom admin class
admin.site.register(CloudService, CloudServiceAdmin)

class ComputeSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_at', 'price_monthly', 'region' ,'unit_price', 'cpu', 'memory' , 'sku' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(ComputeSpecifications, ComputeSpecificationsAdmin)

class StorageSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_at','price_monthly', 'region' ,'unit_price', 'unit_of_storage' ,'sku' ,'provider', 'cloud_service',)
    readonly_fields = ['created_at']  # Prevent editing of 'created_at' field
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(StorageSpecifications, StorageSpecificationsAdmin)

class NetworkingSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_at','price_monthly', 'region' ,'unit_price', 'unit_of_measure' ,'sku' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(NetworkingSpecifications, NetworkingSpecificationsAdmin)

class DatabaseSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_at','price_monthly','region' ,'unit_price', 'unit_of_storage', 'sku' , 'data_type' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(DatabaseSpecifications, DatabaseSpecificationsAdmin)
