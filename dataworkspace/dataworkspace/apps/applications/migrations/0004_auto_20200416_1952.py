# Generated by Django 3.0.5 on 2020-04-16 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("applications", "0003_auto_20200415_1143")]

    operations = [
        migrations.AlterField(
            model_name="applicationtemplate",
            name="nice_name",
            field=models.CharField(max_length=128, verbose_name="application"),
        )
    ]
