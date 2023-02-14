# Generated by Django 3.2.4 on 2021-10-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0091_visualisationlinksqlquery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataset",
            name="user_access_type",
            field=models.CharField(
                choices=[
                    (
                        "OPEN",
                        "Everyone - for public data only, suitable to be shown in demos",
                    ),
                    ("REQUIRES_AUTHENTICATION", "All logged in users"),
                    (
                        "REQUIRES_AUTHORIZATION",
                        "Only specific authorized users or email domains",
                    ),
                ],
                default="REQUIRES_AUTHORIZATION",
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="visualisationcatalogueitem",
            name="user_access_type",
            field=models.CharField(
                choices=[
                    (
                        "OPEN",
                        "Everyone - for public data only, suitable to be shown in demos",
                    ),
                    ("REQUIRES_AUTHENTICATION", "All logged in users"),
                    (
                        "REQUIRES_AUTHORIZATION",
                        "Only specific authorized users or email domains",
                    ),
                ],
                default="REQUIRES_AUTHENTICATION",
                max_length=64,
            ),
        ),
    ]
