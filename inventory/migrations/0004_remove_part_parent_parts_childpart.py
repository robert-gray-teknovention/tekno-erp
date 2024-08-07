# Generated by Django 4.1.6 on 2023-04-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_part_parent_part_part_parent_parts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='parent_parts',
        ),
        migrations.CreateModel(
            name='ChildPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('parent_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_parts', to='inventory.part')),
            ],
        ),
    ]
