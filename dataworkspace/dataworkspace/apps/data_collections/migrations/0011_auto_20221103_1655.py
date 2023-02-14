# Generated by Django 3.2.15 on 2022-11-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_collections", "0010_auto_20221102_0955"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="collectiondatasetmembership",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted", False)),
                fields=("dataset_id", "collection_id"),
                name="unique_dataset_if_not_deleted",
            ),
        ),
        migrations.AddConstraint(
            model_name="collectionvisualisationcatalogueitemmembership",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted", False)),
                fields=("visualisation", "collection_id"),
                name="unique_visualisation_if_not_deleted",
            ),
        ),
    ]
