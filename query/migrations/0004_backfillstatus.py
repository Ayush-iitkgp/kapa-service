# Generated by Django 4.2.7 on 2024-06-04 19:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("query", "0003_remove_labelreview_new_category_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BackfillStatus",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "thread",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="backfill_status",
                        serialize=False,
                        to="query.thread",
                    ),
                ),
                ("is_backfilled", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Backfill Status",
                "verbose_name_plural": "Backfill Statuses",
            },
        ),
    ]
