# Generated by Django 3.2.16 on 2022-12-30 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_timesheetuser_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheetuser',
            name='approvees',
            field=models.ManyToManyField(blank=True, related_name='_employee_timesheetuser_approvees_+', to='employee.TimesheetUser'),
        ),
        migrations.AddField(
            model_name='timesheetuser',
            name='is_approver',
            field=models.BooleanField(default=False),
        ),
    ]