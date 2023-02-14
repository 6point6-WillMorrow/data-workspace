# Generated by Django 3.2.4 on 2021-09-22 19:03

import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0090_referencedataset_licence_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="VisualisationLinkSqlQuery",
            fields=[
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("modified_date", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("data_set_id", models.UUIDField()),
                ("sql_query", models.TextField()),
                ("is_latest", models.BooleanField()),
                (
                    "visualisation_link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sql_queries",
                        to="datasets.visualisationlink",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
