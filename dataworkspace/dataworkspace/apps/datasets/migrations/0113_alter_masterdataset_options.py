# Generated by Django 3.2.12 on 2022-04-19 10:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0112_pendingauthorizedusers"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="masterdataset",
            options={
                "permissions": [
                    (
                        "manage_unpublished_master_datasets",
                        "Manage (create, view, edit) unpublished source datasets",
                    )
                ],
                "verbose_name": "Source Dataset",
            },
        ),
    ]
