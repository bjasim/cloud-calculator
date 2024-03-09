# from django.utils import timezone
# from django.db import models


# # Create your models here.
# class Provider(models.Model):
#     name = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)


# # Cloud Service Table
# class CloudService(models.Model):
#     provider = models.ForeignKey(Provider, related_name='services', on_delete=models.CASCADE)
#     service_type = models.CharField(max_length=100)  # e.g., Compute, Storage, Networking, Database
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

    
# # Compute Specifications Table
# class ComputeSpecifications(models.Model):
#     cloud_service = models.ForeignKey(CloudService, related_name='compute_specs', on_delete=models.CASCADE, null=True)
#     sku = models.CharField(max_length=100, unique=True, default='SKU not provided')  # SKU should be unique
#     instance_type = models.CharField(max_length=50, default='No type provided.')
#     operating_system = models.CharField(max_length=50, default='Ubuntu Pro')
#     cpu = models.CharField(max_length=50)  
#     memory = models.CharField(max_length=50)
#     network_performance = models.CharField(max_length=50, default='No network provided.')
#     tenancy = models.CharField(max_length=50, default='No description provided.')
#     description = models.TextField(default='No description provided.')
#     price_per_unit = models.DecimalField(max_digits=10, decimal_places=7)  # New field for price
#     currency = models.CharField(max_length=10, default='USD')  # New field for currency
#     created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)




# # Storage Specifications Table
# class StorageSpecifications(models.Model):
#     # cloud_service = models.ForeignKey(CloudService, related_name='storage_specs', on_delete=models.CASCADE)
#     storage_class = models.CharField(max_length=50)
#     sku = models.CharField(max_length=100, unique=True, default='SKU not provided')  # SKU should be unique
#     description = models.TextField(default='No description provided.')
#     durability = models.CharField(max_length=50)
#     service_code = models.CharField(max_length=50, default='No code provided.')
#     storage_class = models.CharField(max_length=50, default='No class provided.')
#     price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)  # Hourly price
#     volume_type = models.CharField(max_length=50, default='No type provided.')  # e.g., General Purpose SSD, Provisioned IOPS SSD
#     created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)



# # Networking Specifications Table
# class NetworkingSpecifications(models.Model):
#     cloud_service = models.ForeignKey(CloudService, related_name='networking_specs', on_delete=models.CASCADE)
#     bandwidth = models.CharField(max_length=50)
#     technology = models.CharField(max_length=50)  # e.g., VPC, CDN, Direct Connect
#     created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)




# class DatabaseSpecifications(models.Model):
#     # cloud_service = models.ForeignKey(CloudService, related_name='database_instances', on_delete=models.CASCADE)
#     product = models.CharField(max_length=50, default='No product provided.')  # e.g., MySQL, PostgreSQL, MongoDB
#     db_engine = models.CharField(max_length=50)  # e.g., MySQL, PostgreSQL, MongoDB
#     instance_type = models.CharField(max_length=50, default='No type provided.')
#     instance_sku = models.CharField(max_length=100, default='No SKU provided.')  # SKU for the database instance
#     cpu = models.CharField(max_length=50, default='No cpu provided.')  
#     memory = models.CharField(max_length=50, default='No memory provided.')
#     network_performance = models.CharField(max_length=50, default='No network provided.')
#     description = models.TextField(default='No description provided.')
#     instance_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Hourly price
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class DatabaseStorageVolume(models.Model):
#     # instance = models.ForeignKey(DatabaseSpecifications, related_name='storage_volumes', on_delete=models.CASCADE)
#     description = models.TextField(default='No description provided.')
#     volume_type = models.CharField(max_length=50, default='No type provided.')  # e.g., General Purpose SSD, Provisioned IOPS SSD
#     volume_sku = models.CharField(max_length=100, default='No SKU provided.')  # SKU for the storage
#     storage_capacity = models.CharField(max_length=50, default='Inf')  # e.g., '200 GB', '1 TB'
#     max_iops = models.IntegerField(null=True, blank=True)  # Optional field
#     volume_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)  # Monthly price per GB with higher precision
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# # class DatabaseSpecifications(models.Model):
# #     cloud_service = models.ForeignKey(CloudService, related_name='database_specs', on_delete=models.CASCADE)
# #     db_engine = models.CharField(max_length=50)  # e.g., MySQL, PostgreSQL, MongoDB
# #     instance_type = models.CharField(max_length=50, default='No type provided.')
# #     volume_type = models.CharField(max_length=50, default='No type provided.')  # e.g., General Purpose SSD, Provisioned IOPS SSD
# #     storage_capacity = models.CharField(max_length=50)  # e.g., '200 GB', '1 TB'
# #     max_iops = models.IntegerField()
# #     instance_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Hourly price
# #     volume_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Monthly price per GB
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     @property
# #     def final_price(self):
# #         monthly_instance_cost = self.instance_price * 730  # Convert hourly price to monthly
# #         return monthly_instance_cost + self.volume_price  # Total monthly cost
from django.db import models

# Create your models here.
