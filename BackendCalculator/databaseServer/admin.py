from django.contrib import admin
from .models import Provider, CloudService, ComputeSpecifications, StorageSpecifications, NetworkingSpecifications, DatabaseSpecifications

# Register your models here.
admin.site.register(Provider)
admin.site.register(CloudService)

class ComputeSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'unit_price' , 'sku' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(ComputeSpecifications, ComputeSpecificationsAdmin)

class StorageSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'unit_price' ,'sku' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(StorageSpecifications, StorageSpecificationsAdmin)

class NetworkingSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'unit_price' ,'sku' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(NetworkingSpecifications, NetworkingSpecificationsAdmin)

class DatabaseSpecificationsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'unit_price', 'sku' , 'data_type' ,'provider', 'cloud_service',)
    list_display_links = ('name',)  # Make the name field clickable

admin.site.register(DatabaseSpecifications, DatabaseSpecificationsAdmin)
