from django.db import models


class Car(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
