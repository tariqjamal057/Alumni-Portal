# Generated by Django 4.0 on 2021-12-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0018_remove_event_budjet'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='budjet',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='main_event',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
