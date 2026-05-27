from decimal import Decimal

from django.db import migrations


def seed_inventory(apps, schema_editor):
    FlowerInventory = apps.get_model("inventory", "FlowerInventory")
    FlowerInventory.objects.bulk_create(
        [
            FlowerInventory(
                type_of_flower="Rose",
                quantity=250,
                cost=Decimal("2.50"),
            ),
            FlowerInventory(
                type_of_flower="Tulip",
                quantity=180,
                cost=Decimal("1.25"),
            ),
            FlowerInventory(
                type_of_flower="Lily",
                quantity=120,
                cost=Decimal("3.00"),
            ),
            FlowerInventory(
                type_of_flower="Sunflower",
                quantity=90,
                cost=Decimal("2.00"),
            ),
        ]
    )


def remove_seed_inventory(apps, schema_editor):
    FlowerInventory = apps.get_model("inventory", "FlowerInventory")
    FlowerInventory.objects.filter(
        type_of_flower__in=["Rose", "Tulip", "Lily", "Sunflower"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_inventory, remove_seed_inventory),
    ]
