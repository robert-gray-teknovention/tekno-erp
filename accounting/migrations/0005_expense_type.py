# Generated by Django 4.2.6 on 2024-07-25 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_alter_expense_total_cost_alter_mileage_entry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.CharField(choices=[('MILEAGE', 'Mileage'), ('MEALS', 'Meals'), ('TRANSPORTATION', 'Transportation'), ('LODGING', 'Lodging')], max_length=20, null=True),
        ),
    ]