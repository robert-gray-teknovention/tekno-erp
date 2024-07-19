# Generated by Django 4.1.6 on 2023-05-21 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0014_rename_email_organization_mailer_email'),
        ('purchasing', '0034_alter_vendor_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.RemoveField(
            model_name='manufacturer',
            name='organization',
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization'),
        ),
    ]