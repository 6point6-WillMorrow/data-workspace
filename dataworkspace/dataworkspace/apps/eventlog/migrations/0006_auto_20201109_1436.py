# Generated by Django 3.0.8 on 2020-11-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventlog", "0005_auto_20200416_1441"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventlog",
            name="event_type",
            field=models.IntegerField(
                choices=[
                    (1, "Dataset source link download"),
                    (2, "Dataset source table download"),
                    (3, "Reference dataset download"),
                    (4, "Table data download"),
                    (5, "SQL query download"),
                    (6, "Dataset source view download"),
                    (7, "Visualisation approved"),
                    (8, "Visualisation unapproved"),
                    (9, "Dataset access request"),
                    (10, "Granted dataset permission"),
                    (11, "Revoked dataset permission"),
                    (12, "Granted user permission"),
                    (13, "Revoked user permission"),
                    (14, "Granted visualisation permission"),
                    (15, "Revoked visualisation permission"),
                    (16, "Set dataset user access type"),
                    (17, "View AWS QuickSight visualisation"),
                    (18, "View Google DataStudio visualisation"),
                    (19, "Saved a query in Data Explorer"),
                ]
            ),
        ),
    ]
