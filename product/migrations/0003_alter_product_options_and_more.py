# Generated by Django 4.2.9 on 2024-01-07 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_expiration_product_manufacturer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='expiration',
            new_name='expiration_yyyymmdd',
        ),
    ]
