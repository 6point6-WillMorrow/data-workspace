# Generated by Django 3.0.5 on 2020-04-16 19:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("datasets", "0040_visualisationcatalogueitem")]

    operations = [
        migrations.AlterModelOptions(
            name="visualisationcatalogueitem",
            options={
                "permissions": [
                    (
                        "manage_unpublished_visualisations",
                        "Manage (create, view, edit) unpublished visualisations",
                    )
                ]
            },
        )
    ]
