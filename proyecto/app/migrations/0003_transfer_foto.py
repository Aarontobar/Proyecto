# Generated by Django 5.0.6 on 2024-06-25 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_transfer_conductor'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]