# Generated by Django 4.2.6 on 2024-07-24 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0016_timesheetentry_project'),
        ('projects', '0003_alter_project_finished_date'),
        ('accounting', '0003_alter_mileage_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='mileage',
            name='entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timesheets.timesheetentry'),
        ),
        migrations.AlterField(
            model_name='mileage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
