# Generated by Django 3.2.5 on 2021-12-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0103_merge_0102_auto_20211210_2106_0102_auto_20211215_0909"),
    ]

    operations = [
        migrations.AddField(
            model_name="referencedataset",
            name="is_draft",
            field=models.BooleanField(default=False),
        ),
    ]
