# Generated by Django 2.1.7 on 2020-06-28 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='categroy',
            new_name='category',
        ),
    ]
