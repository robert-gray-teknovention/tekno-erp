# Generated by Django 4.1.6 on 2023-04-12 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0014_rename_email_organization_mailer_email'),
        ('purchasing', '0023_remove_purchaseitem_organization_item_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization'),
        ),
    ]