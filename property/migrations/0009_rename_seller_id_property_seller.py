# Generated by Django 5.2 on 2025-05-11 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_property_seller_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='seller_id',
            new_name='seller',
        ),
    ]
