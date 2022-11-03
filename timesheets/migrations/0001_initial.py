# Generated by Django 3.2.16 on 2022-11-03 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0003_timesheetuser_hourly_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimesheetEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_entry', models.DateTimeField(auto_now_add=True)),
                ('date_time_in', models.DateTimeField()),
                ('date_time_out', models.DateTimeField()),
                ('duration', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.timesheetuser')),
            ],
        ),
    ]