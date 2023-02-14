# Generated by Django 3.2.10 on 2022-01-07 13:02

from django.db import migrations, models
import dataworkspace.apps.core.storage


class Migration(migrations.Migration):
    dependencies = [
        ("explorer", "0017_chartbuilderchart"),
    ]

    operations = [
        migrations.AddField(
            model_name="chartbuilderchart",
            name="thumbnail",
            field=models.FileField(
                blank=True,
                null=True,
                storage=dataworkspace.apps.core.storage.S3FileStorage(
                    location="chart-builder-thumbnails"
                ),
                upload_to="",
            ),
        ),
    ]
