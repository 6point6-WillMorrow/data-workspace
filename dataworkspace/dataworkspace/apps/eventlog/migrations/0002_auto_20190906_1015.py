# Generated by Django 2.2.3 on 2019-09-06 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0001_initial_squashed_0002_auto_20190816_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='event_type',
            field=models.IntegerField(
                choices=[
                    (1, 'Dataset source link download'),
                    (2, 'Dataset source table download'),
                    (3, 'Reference dataset download'),
                    (4, 'Table data download'),
                    (5, 'SQL query download')
                ]
            ),
        ),
    ]
