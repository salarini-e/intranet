# Generated by Django 4.2.16 on 2025-01-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_de_ponto', '0002_responsavel'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='ip_inclusao',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
