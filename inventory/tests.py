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

    def test_swagger_json_documents_inventory_endpoint(self):
        response = self.client.get("/swagger.json")

        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertEqual(schema["openapi"], "3.0.3")
        self.assertIn("/inventory/", schema["paths"])
        self.assertIn("get", schema["paths"]["/inventory/"])
        self.assertIn("post", schema["paths"]["/inventory/"])

    def test_swagger_ui_loads_openapi_schema(self):
        response = self.client.get("/swagger/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SwaggerUIBundle")
        self.assertContains(response, "/swagger.json")
