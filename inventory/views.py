import json
from decimal import Decimal

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import FlowerInventory
from .openapi import OPENAPI_SCHEMA, SWAGGER_UI_HTML


def serialize_inventory_item(item, purchased_quantity=None):
    data = {
        "id": item.id,
        "type_of_flower": item.type_of_flower,
        "description": item.description,
        "quantity": item.quantity,
        "cost": str(item.cost),
    }
    if purchased_quantity is not None:
        data["purchased_quantity"] = purchased_quantity
        data["purchase_total"] = str(item.cost * Decimal(purchased_quantity))
    return data


def swagger_json(request):
    return JsonResponse(OPENAPI_SCHEMA)


def swagger_ui(request):
    return HttpResponse(SWAGGER_UI_HTML)


@csrf_exempt
def inventory(request):
    if request.method == "GET":
        items = FlowerInventory.objects.all()
        return JsonResponse(
            {"inventory": [serialize_inventory_item(item) for item in items]}
        )

    if request.method == "POST":
        try:
            body = json.loads(request.body or "{}")
            item_id = body["id"]
            purchase_quantity = int(body.get("quantity", 1))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return JsonResponse(
                {"error": "Send JSON with an inventory id and optional quantity."},
                status=400,
            )

        if purchase_quantity < 1:
            return JsonResponse(
                {"error": "Purchase quantity must be at least 1."},
                status=400,
            )

        with transaction.atomic():
            item = FlowerInventory.objects.select_for_update().filter(id=item_id).first()
            if item is None:
                return JsonResponse({"error": "Inventory item not found."}, status=404)

            if item.quantity < purchase_quantity:
                return JsonResponse(
                    {"error": "Not enough flowers available for that purchase."},
                    status=400,
                )

            item.quantity -= purchase_quantity
            item.save(update_fields=["quantity"])

        return JsonResponse({"purchased": serialize_inventory_item(item, purchase_quantity)})

    return JsonResponse({"error": "Use GET or POST."}, status=405)
