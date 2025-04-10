# Generated by Django 5.1.6 on 2025-03-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models_app", "0008_photo_prev_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=511, verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "db_table": "notification",
            },
        ),
    ]
