from django.urls import path

from inventory.views import inventory, swagger_json, swagger_ui

urlpatterns = [
    path("inventory/", inventory, name="inventory"),
    path("swagger/", swagger_ui, name="swagger-ui"),
    path("swagger.json", swagger_json, name="swagger-json"),
]
