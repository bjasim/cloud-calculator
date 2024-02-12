from django.db import models



# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=100)


# Cloud Service Table
class CloudService(models.Model):
    provider = models.ForeignKey(Provider, related_name='services', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)  # e.g., Compute, Storage, Networking, Database
    description = models.TextField()
    
# Compute Specifications Table
class ComputeSpecifications(models.Model):
    cloud_service = models.ForeignKey(CloudService, related_name='compute_specs', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True, default='SKU not provided')  # SKU should be unique
    instance_type = models.CharField(max_length=50, default='No type provided.')
    operating_system = models.CharField(max_length=50, default='Ubuntu Pro')
    cpu = models.CharField(max_length=50)  
    memory = models.CharField(max_length=50)
    network_performance = models.CharField(max_length=50, default='No network provided.')
    tenancy = models.CharField(max_length=50, default='No description provided.')
    description = models.TextField(default='No description provided.')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=7)  # New field for price
    currency = models.CharField(max_length=10, default='USD')  # New field for currency



# Storage Specifications Table
class StorageSpecifications(models.Model):
    cloud_service = models.ForeignKey(CloudService, related_name='storage_specs', on_delete=models.CASCADE)
    storage_class = models.CharField(max_length=50)
    redundancy = models.CharField(max_length=50)
    durability = models.CharField(max_length=50)


# Networking Specifications Table
class NetworkingSpecifications(models.Model):
    cloud_service = models.ForeignKey(CloudService, related_name='networking_specs', on_delete=models.CASCADE)
    bandwidth = models.CharField(max_length=50)
    technology = models.CharField(max_length=50)  # e.g., VPC, CDN, Direct Connect


# Database Specifications Table
class DatabaseSpecifications(models.Model):
    cloud_service = models.ForeignKey(CloudService, related_name='database_specs', on_delete=models.CASCADE)
    db_engine = models.CharField(max_length=50)  # e.g., MySQL, PostgreSQL, MongoDB
    storage_capacity = models.CharField(max_length=50)
    max_iops = models.IntegerField()
