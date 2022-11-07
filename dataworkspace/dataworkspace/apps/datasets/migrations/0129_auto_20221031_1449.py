# Generated by Django 3.2.15 on 2022-10-31 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("datasets", "0128_auto_20220616_1649"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferenceDatasetInheritingFromDataSet",
            fields=[],
            options={
                "verbose_name": "Reference dataset inheriting from dataset",
                "verbose_name_plural": "Reference datasets inheriting from datasets",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("datasets.dataset",),
        ),
        migrations.AlterField(
            model_name="dataset",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Master Dataset"), (2, "Data Cut"), (0, "Reference Dataset")],
                default=2,
            ),
        ),
        migrations.AddField(
            model_name="referencedataset",
            name="reference_dataset_inheriting_from_dataset",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="datasets.referencedatasetinheritingfromdataset",
                unique=True,
            ),
        ),
    ]