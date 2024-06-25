# Generated by Django 5.0.6 on 2024-06-25 06:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=150, unique=True)),
                ('contrasenna', models.CharField(max_length=128)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('horario_entrada', models.TimeField()),
                ('horario_salida', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_agre', models.DateTimeField(default=django.utils.timezone.now)),
                ('transfers', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('horario_entrada', models.TimeField()),
                ('horario_salida', models.TimeField()),
                ('rol', models.CharField(blank=True, choices=[('admin_aeropuerto', 'Admin Aeropuerto'), ('admin_empresa_transfer', 'Admin Empresa Transfer'), ('superuser', 'Superuser')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='transfer',
            fields=[
                ('patente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('capacidad', models.IntegerField()),
                ('disponible', models.BooleanField(default=True)),
                ('conductor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.empresatransfer')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_realizacion', models.DateField()),
                ('hora_realizacion', models.TimeField()),
                ('destino', models.CharField(max_length=200)),
                ('cantidad_asientos', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cliente')),
                ('transfer_utilizado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.transfer')),
            ],
        ),
    ]
