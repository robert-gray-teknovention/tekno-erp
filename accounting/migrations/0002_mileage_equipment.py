# Generated by Django 4.2.6 on 2024-07-24 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_alter_serialpart_man_serial_number_and_more'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mileage',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.equipment'),
        ),
    ]
