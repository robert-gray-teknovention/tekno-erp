# Generated by Django 4.2.6 on 2024-09-19 19:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_alter_expense_accrue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='accrue_date',
            field=models.DateField(default=datetime.datetime(2024, 9, 19, 19, 48, 6, 968756)),
        ),
    ]
