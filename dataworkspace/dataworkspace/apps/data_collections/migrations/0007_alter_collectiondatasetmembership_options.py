# Generated by Django 3.2.15 on 2022-10-31 13:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data_collections", "0006_auto_20221031_1229"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collectiondatasetmembership",
            options={"ordering": ("id",)},
        ),
    ]
