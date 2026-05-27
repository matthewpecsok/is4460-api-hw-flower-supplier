import json

from django.test import TestCase

from .models import FlowerInventory


class InventoryApiTests(TestCase):
    def setUp(self):
        FlowerInventory.objects.all().delete()

    def test_get_lists_inventory(self):
        item = FlowerInventory.objects.create(
            type_of_flower="Tulip",
            quantity=50,
            cost="1.25",
        )

        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "inventory": [
                    {
                        "id": item.id,
                        "type_of_flower": "Tulip",
                        "quantity": 50,
                        "cost": "1.25",
                    }
                ]
            },
        )

    def test_post_purchases_inventory(self):
        item = FlowerInventory.objects.create(
            type_of_flower="Rose",
            quantity=100,
            cost="2.50",
        )

        response = self.client.post(
            "/inventory/",
            data=json.dumps({"id": item.id, "quantity": 12}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "purchased": {
                    "id": item.id,
                    "type_of_flower": "Rose",
                    "quantity": 88,
                    "cost": "2.50",
                    "purchased_quantity": 12,
                    "purchase_total": "30.00",
                }
            },
        )

        item.refresh_from_db()
        self.assertEqual(item.quantity, 88)
