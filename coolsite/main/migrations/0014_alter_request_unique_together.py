# Generated by Django 4.2 on 2023-05-02 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_request_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='request',
            unique_together=set(),
        ),
    ]
