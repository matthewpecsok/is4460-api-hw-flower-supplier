from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FlowerInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_of_flower", models.CharField(max_length=100)),
                ("quantity", models.PositiveIntegerField()),
                ("cost", models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                "verbose_name_plural": "flower inventory",
                "ordering": ["type_of_flower"],
            },
        ),
    ]
