# Generated by Django 5.1.3 on 2024-11-19 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("models_app", "0005_alter_photo_photo"),
    ]

    operations = [
        migrations.RenameField(
            model_name="photo",
            old_name="caption",
            new_name="description",
        ),
    ]
