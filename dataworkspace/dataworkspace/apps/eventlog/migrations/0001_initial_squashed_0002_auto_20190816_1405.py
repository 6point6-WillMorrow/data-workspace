# Generated by Django 2.2.3 on 2019-08-20 14:54

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EventLog",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("timestamp", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "event_type",
                    models.IntegerField(
                        choices=[
                            (1, "Dataset source link download"),
                            (2, "Dataset source table download"),
                            (3, "Reference dataset download"),
                            (4, "Table data download"),
                        ]
                    ),
                ),
                ("object_id", models.CharField(max_length=255, null=True)),
                (
                    "extra",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-timestamp",), "get_latest_by": "timestamp"},
        )
    ]
