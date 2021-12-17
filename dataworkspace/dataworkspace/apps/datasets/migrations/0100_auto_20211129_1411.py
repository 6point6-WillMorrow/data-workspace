# Generated by Django 3.2.5 on 2021-11-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0099_alter_tag_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="acronyms",
            field=models.CharField(default="", max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="referencedataset",
            name="acronyms",
            field=models.CharField(default="", max_length=255, blank=True),
            preserve_default=True,
        ),
    ]