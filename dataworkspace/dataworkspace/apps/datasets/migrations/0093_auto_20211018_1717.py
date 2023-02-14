# Generated by Django 3.2.4 on 2021-10-18 17:17

import django.contrib.postgres.search
import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0092_auto_20211007_1219"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="referencedataset",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="visualisationcatalogueitem",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True, blank=True),
        ),
        migrations.AddIndex(
            model_name="dataset",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="app_dataset_search__d970dd_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="referencedataset",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="app_referen_search__d655d7_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="visualisationcatalogueitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="datasets_vi_search__d20f56_gin"
            ),
        ),
    ]
