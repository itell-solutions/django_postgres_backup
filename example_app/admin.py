from django.contrib import admin

from example_app.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name",)
