# Generated by Django 4.1.6 on 2023-04-16 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_part_child_parts_alter_childpart_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SerialPart',
        ),
    ]