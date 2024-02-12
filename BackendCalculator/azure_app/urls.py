from django.urls import path
from . import views

urlpatterns = [
    path('get-pricing/', views.get_pricing, name='get_pricing'),
]
