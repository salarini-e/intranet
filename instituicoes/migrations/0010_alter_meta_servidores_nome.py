# Generated by Django 4.2.11 on 2024-04-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instituicoes', '0009_meta_servidores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta_servidores',
            name='nome',
            field=models.CharField(max_length=164, verbose_name='Nome'),
        ),
    ]
