# Generated by Django 3.2.7 on 2021-10-24 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='paid_ammount',
            new_name='paid_amount',
        ),
    ]
