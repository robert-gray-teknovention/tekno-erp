# Generated by Django 4.1.6 on 2023-07-10 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0016_invitee_status_date_alter_invitee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitee',
            name='authentication_code',
            field=models.CharField(max_length=15),
        ),
    ]
