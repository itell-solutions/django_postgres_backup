# Register your models here.
from django.contrib import admin

from example_app.models import Cars


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name",)
