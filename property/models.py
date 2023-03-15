from django.db import models

class Property(models.Model):
    """
    Table Imported from BigQuery Dataset (Property Data)
    """

    id = models.CharField(max_length=50, primary_key=True)
    created_on = models.DateTimeField()
    operation = models.CharField(max_length=10, null=True)
    property_type = models.CharField(max_length=50, null=True)
    place_name = models.CharField(max_length=100, null=True)
    place_with_parent_names = models.TextField()
    country_name = models.CharField(max_length=50, null=True)
    state_name = models.CharField(max_length=50, null=True)
    geonames_id = models.CharField(max_length=50, null=True)
    lat_lon = models.CharField(max_length=50, null=True)
    lat = models.CharField(max_length=100, null=True)
    lon = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    currency = models.CharField(max_length=5, null=True)
    price_aprox_local_currency = models.CharField(max_length=100, null=True)
    price_aprox_usd = models.CharField(max_length=100, null=True)
    surface_total_in_m2 = models.CharField(max_length=100, null=True)
    surface_covered_in_m2 = models.CharField(max_length=100, null=True)
    price_usd_per_m2 = models.CharField(max_length=100, null=True)
    price_per_m2 = models.CharField(max_length=100, null=True)
    floor = models.CharField(max_length=100, null=True)
    rooms = models.CharField(max_length=100, null=True)
    expenses = models.CharField(max_length=100, null=True)
    properati_url = models.TextField()
    description = models.TextField()
    title = models.CharField(max_length=200, null=True)
    image_thumbnail = models.TextField()

    class Meta:
        db_table = 'property'
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title
