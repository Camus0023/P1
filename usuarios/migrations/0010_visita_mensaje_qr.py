# Generated by Django 5.0.7 on 2024-11-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_visita_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='visita',
            name='mensaje_qr',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]