# Generated by Django 4.2.6 on 2024-08-02 15:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_alter_expense_accrue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='accrue_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 4, 37, 748176)),
        ),
    ]
