# Generated by Django 3.2.15 on 2022-10-31 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0128_auto_20220616_1649"),
        ("data_collections", "0005_rename_uuid_collection_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionDatasetMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("modified_date", models.DateTimeField(auto_now=True)),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collections",
                        to="data_collections.collection",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="datasets",
                        to="datasets.dataset",
                    ),
                ),
            ],
            options={
                "unique_together": {("dataset_id", "collection_id")},
            },
        ),
        migrations.AddField(
            model_name="collection",
            name="datasets",
            field=models.ManyToManyField(
                through="data_collections.CollectionDatasetMembership", to="datasets.DataSet"
            ),
        ),
    ]
