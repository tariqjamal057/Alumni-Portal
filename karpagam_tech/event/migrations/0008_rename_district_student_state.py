# Generated by Django 4.0 on 2021-12-17 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='district',
            new_name='state',
        ),
    ]
