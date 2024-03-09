from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Cloud Service Table
class CloudService(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False)
    service_type = models.CharField(max_length=100)  # e.g., Compute, Storage, Networking, Database
    description = models.TextField()

    def __str__(self):
        return f"{self.provider.name} {self.service_type}"


# Compute Specifications Table
class ComputeSpecifications(models.Model):
    name = models.CharField(max_length=100, default='')  # Provide default value
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False, default=1)
    cloud_service = models.ForeignKey(CloudService, related_name='compute_specs', on_delete=models.CASCADE, null=False)
    sku = models.CharField(max_length=100, unique=True, default='SKU not provided')
    instance_type = models.CharField(max_length=50, default='No type provided.')
    operating_system = models.CharField(max_length=50, default='Ubuntu Pro')
    cpu = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    network_performance = models.CharField(max_length=50, default='No network provided.')
    tenancy = models.CharField(max_length=50, default='No description provided.')
    description = models.TextField(default='No description provided.')
    unit_price = models.CharField(max_length=50,default='0.0')
    currency = models.CharField(max_length=10, default='USD')
    region = models.CharField(max_length=50, default='No region provided')
    price_monthly = models.CharField(max_length=50,default='0.0')



    def __str__(self):
        return self.name if self.name else 'Unnamed Compute Specification'

# Storage Specifications Table
class StorageSpecifications(models.Model):
    name = models.CharField(max_length=100, default='')  # Provide default value
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False, default=1)
    cloud_service = models.ForeignKey(CloudService, related_name='storage_specs', on_delete=models.CASCADE, null=False)
    # Like standard storage, hot storage or cool storage.
    sku = models.CharField(max_length=50)
    unit_price = models.CharField(max_length=50)
    unit_of_storage = models.CharField(max_length=50)
    region = models.CharField(max_length=50, default='No region provided')
    description = models.TextField(blank=True, default='')
    durability = models.CharField(max_length=50, default='No durability provided.')
    service_code = models.CharField(max_length=50, default='No code provided.')
    storage_class = models.CharField(max_length=50, default='No class provided.')
    volume_type = models.CharField(max_length=50, default='No type provided.')  # e.g., General Purpose SSD, Provisioned IOPS SSD
    price_monthly = models.CharField(max_length=50,default='0.0')


    def __str__(self):
        return self.name if self.name else 'Unnamed Storage Specification'

# Networking Specifications Table
class NetworkingSpecifications(models.Model):
    name = models.CharField(max_length=100, default='')  # Provide default value
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False, default=1)
    cloud_service = models.ForeignKey(CloudService, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    unit_price = models.CharField(max_length=50, default='0.0')
    unit_of_measure = models.CharField(max_length=50)
    region = models.CharField(max_length=50, default='No region provided')
    price_monthly = models.CharField(max_length=50,default='0.0')

    def __str__(self):
        return self.name if self.name else 'Unnamed Networking Specification'


# Database Specifications Table
class DatabaseSpecifications(models.Model):
    name = models.CharField(max_length=100, default='')  # Provide default value
    provider = models.ForeignKey(Provider,  on_delete=models.CASCADE, null=False, default=1)
    cloud_service = models.ForeignKey(CloudService, related_name='database_specs', on_delete=models.CASCADE, null=False)
    data_type = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    unit_price = models.CharField(max_length=50, default='0.0')
    unit_of_storage = models.CharField(max_length=50, default ='0.0')
    region = models.CharField(max_length=50, default='No region provided')
    description = models.TextField(blank=True, default='')
    volume_type = models.CharField(max_length=100, blank=True, default='')
    storage_capacity = models.CharField(max_length=100, blank=True, default='')
    product = models.CharField(max_length=50, default='No product provided.')  # e.g., MySQL, PostgreSQL, MongoDB
    instance_type = models.CharField(max_length=50, default='No type provided.')
    db_engine = models.CharField(max_length=50, default='No engine used')  # e.g., MySQL, PostgreSQL, MongoDB
    cpu = models.CharField(max_length=50, default='No cpu provided.')  
    memory = models.CharField(max_length=50, default='No memory provided.')
    network_performance = models.CharField(max_length=50, default='No network provided.')
    price_monthly = models.CharField(max_length=50,default='0.0')


    def __str__(self):
        return self.name if self.name else 'Unnamed Database Specification'
