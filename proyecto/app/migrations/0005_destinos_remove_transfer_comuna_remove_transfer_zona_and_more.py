# Generated by Django 5.0.6 on 2024-06-27 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_reserva_destino_reserva_comuna_reserva_zona_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='destinos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(max_length=100)),
                ('comuna', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='zona',
        ),
        migrations.AddField(
            model_name='transfer',
            name='destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.destinos'),
        ),
    ]
