# Generated by Django 4.2.6 on 2024-07-24 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timesheets', '0016_timesheetentry_project'),
        ('projects', '0003_alter_project_finished_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('expense_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.expense')),
                ('accrue_date', models.DateField(auto_now=True)),
                ('miles', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timesheets.timesheetentry')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('rate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounting.rate')),
            ],
            bases=('accounting.expense',),
        ),
    ]
