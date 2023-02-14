# Generated by Django 2.2.3 on 2019-10-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("eventlog", "0002_auto_20190906_1015")]

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
                ]
            ),
        )
    ]
