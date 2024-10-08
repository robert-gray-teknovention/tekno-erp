# Generated by Django 4.2.6 on 2024-07-15 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0018_alter_serialpart_man_serial_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('acquired_date', models.DateTimeField()),
                ('retired_date', models.DateTimeField(null=True)),
                ('equipment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.asset')),
                ('year_built', models.IntegerField(max_length=4)),
            ],
            bases=('assets.asset',),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.asset')),
                ('mileage', models.DecimalField(decimal_places=1, max_digits=10)),
            ],
            bases=('assets.asset',),
        ),
    ]
