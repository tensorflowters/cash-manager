# Generated by Django 4.1 on 2022-11-15 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_product_in_stock_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
