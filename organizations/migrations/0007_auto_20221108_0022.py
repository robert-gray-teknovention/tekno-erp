# Generated by Django 3.2.16 on 2022-11-08 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_biweeklyperiodtype_monthlyperiodtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='biweeklyperiodtype',
            name='seed_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='monthlyperiodtype',
            name='start_date_of_month',
            field=models.IntegerField(default=1),
        ),
    ]