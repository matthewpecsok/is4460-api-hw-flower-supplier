from django.db import migrations, models


STARTER_DESCRIPTIONS = {
    "Rose": "Classic long-stem roses for bouquets, arrangements, and events.",
    "Tulip": "Bright seasonal tulips with clean stems and vibrant petals.",
    "Lily": "Fragrant lilies suited for premium arrangements and centerpieces.",
    "Sunflower": "Large sunny blooms that add height and warmth to displays.",
}


def add_starter_descriptions(apps, schema_editor):
    FlowerInventory = apps.get_model("inventory", "FlowerInventory")
    for type_of_flower, description in STARTER_DESCRIPTIONS.items():
        FlowerInventory.objects.filter(type_of_flower=type_of_flower).update(
            description=description
        )


def remove_starter_descriptions(apps, schema_editor):
    FlowerInventory = apps.get_model("inventory", "FlowerInventory")
    FlowerInventory.objects.filter(type_of_flower__in=STARTER_DESCRIPTIONS).update(
        description=""
    )


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_seed_inventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="flowerinventory",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.RunPython(add_starter_descriptions, remove_starter_descriptions),
    ]
