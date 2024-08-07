# Generated by Django 4.1.6 on 2023-04-09 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0002_manufacturer_organization_purchaseitem_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturer',
            name='organization',
        ),
        migrations.DeleteModel(
            name='PurchaseHistory',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Manufacturer',
        ),
        migrations.DeleteModel(
            name='PurchaseItem',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]
