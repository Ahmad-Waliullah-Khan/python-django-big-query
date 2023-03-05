from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    """
    Admin View for Property Model (Table Imported from BigQuery Dataset (Property Data))
    """
    list_display = ('id', 'created_on', 'operation', 'property_type', 'place_name', 'price')

admin.site.register(Property, PropertyAdmin)
