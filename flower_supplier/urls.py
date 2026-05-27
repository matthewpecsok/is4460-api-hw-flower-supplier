from django.urls import path

from inventory.views import inventory

urlpatterns = [
    path("inventory/", inventory, name="inventory"),
]
