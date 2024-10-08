# Generated by Django 4.2.6 on 2024-07-16 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_alter_serialpart_man_serial_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serialpart',
            name='man_serial_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='serialpart',
            name='serial_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
