# Generated by Django 3.2.16 on 2023-01-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20230103_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetuser',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
