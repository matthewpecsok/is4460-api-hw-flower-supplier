from django.db import models


class FlowerInventory(models.Model):
    type_of_flower = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["type_of_flower"]
        verbose_name_plural = "flower inventory"

    def __str__(self):
        return f"{self.type_of_flower} ({self.quantity} available)"
