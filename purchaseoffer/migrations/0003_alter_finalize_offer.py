# Generated by Django 5.2 on 2025-05-13 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchaseoffer', '0002_alter_finalize_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalize',
            name='offer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='purchaseoffer.offer'),
        ),
    ]
