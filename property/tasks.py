import csv
from django.core.management.base import BaseCommand
from invoke import task
import django
from datetime import datetime

import os 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adtask.settings")
django.setup()

"""
Method to import csv file from BigQuery TableA into 'property' table in local database
"""
def import_data(filename):
    from property.models import Property
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            created_on = datetime.strptime(row['created_on'], '%m/%d/%Y').strftime('%Y-%m-%d')
            floor = row['floor']
            if floor == '':
                floor = None
            Property.objects.create(
                id=row['id'],
                created_on=created_on,
                operation=row['operation'],
                property_type=row['property_type'],
                place_name=row['place_name'],
                place_with_parent_names=row['place_with_parent_names'],
                country_name=row['country_name'],
                state_name=row['state_name'],
                geonames_id=row['geonames_id'],
                lat_lon=row['lat_lon'],
                lat=row['lat'],
                lon=row['lon'],
                price=row['price'],
                currency=row['currency'],
                price_aprox_local_currency=row['price_aprox_local_currency'],
                price_aprox_usd=row['price_aprox_usd'],
                surface_total_in_m2=row['surface_total_in_m2'],
                surface_covered_in_m2=row['surface_covered_in_m2'],
                price_usd_per_m2=row['price_usd_per_m2'],
                price_per_m2=row['price_per_m2'],
                floor=floor,
                rooms=row['rooms'],
                expenses=row['expenses'],
                properati_url=row['properati_url'],
                description=row['description'],
                title=row['title'],
                image_thumbnail=row['image_thumbnail'],
            )

"""
Invoke task to import csv file from BigQuery TableA into 'property' table in local database
"""
@task
def import_csv(ctx, filename):
    import_data(filename)
