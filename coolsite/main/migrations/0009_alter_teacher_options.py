# Generated by Django 4.1.7 on 2023-03-26 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_remove_request_is_approved"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teacher",
            options={
                "ordering": ["name"],
                "verbose_name": "Преподаватель",
                "verbose_name_plural": "Преподаватели",
            },
        ),
    ]
