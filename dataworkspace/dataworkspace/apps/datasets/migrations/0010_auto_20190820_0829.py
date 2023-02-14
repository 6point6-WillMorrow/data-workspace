# Generated by Django 2.2.3 on 2019-08-20 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial"), ("datasets", "0009_auto_20190819_1227")]

    operations = [
        migrations.AddField(
            model_name="referencedataset",
            name="external_database",
            field=models.ForeignKey(
                blank=True,
                help_text="Name of the analysts database to keep in sync with this reference dataset",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.Database",
            ),
        )
    ]
