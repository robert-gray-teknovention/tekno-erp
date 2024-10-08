# Generated by Django 4.2.6 on 2024-09-20 07:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0041_vendor_type'),
        ('accounting', '0028_remove_meals_expense_ptr_remove_misc_expense_ptr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lodging',
            fields=[
                ('vendorexpense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.vendorexpense')),
                ('nightly_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nights', models.IntegerField(default=1)),
            ],
            bases=('accounting.vendorexpense',),
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('vendorexpense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.vendorexpense')),
                ('meal_type', models.CharField(choices=[('RESTAURANT', 'Restaurant'), ('GROCERIES', 'Groceries')], max_length=20, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tip', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
            bases=('accounting.vendorexpense',),
        ),
        migrations.CreateModel(
            name='Misc',
            fields=[
                ('vendorexpense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.vendorexpense')),
            ],
            bases=('accounting.vendorexpense',),
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('vendorexpense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.vendorexpense')),
                ('transportation_type', models.CharField(choices=[('BUS', 'Bus'), ('AIR', 'Airfare'), ('TAXI', 'Taxi'), ('RIDE', 'Rideshare'), ('TRAIN', 'Train')], max_length=10, null=True)),
            ],
            bases=('accounting.vendorexpense',),
        ),
        migrations.AlterField(
            model_name='expense',
            name='accrue_date',
            field=models.DateField(default=datetime.datetime(2024, 9, 20, 7, 34, 23, 450771)),
        ),
        migrations.CreateModel(
            name='ServiceExpense',
            fields=[
                ('vendorexpense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.vendorexpense')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.service')),
            ],
            bases=('accounting.vendorexpense',),
        ),
    ]
