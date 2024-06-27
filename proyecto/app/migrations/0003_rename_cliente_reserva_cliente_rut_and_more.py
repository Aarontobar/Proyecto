# Generated by Django 5.0.6 on 2024-06-27 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_reserva_cliente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserva',
            old_name='cliente',
            new_name='cliente_rut',
        ),
        migrations.AlterField(
            model_name='reserva',
            name='transfer_utilizado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.transfer'),
        ),
    ]