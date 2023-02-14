# Generated by Django 3.2.16 on 2022-11-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0131_refesh_reference_dataset_inhertance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataset",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Source Dataset"), (2, "Data Cut"), (0, "Reference Dataset")],
                default=2,
            ),
        ),
    ]
