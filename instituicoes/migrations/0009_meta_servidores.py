# Generated by Django 4.2.11 on 2024-04-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instituicoes', '0008_servidor_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meta_Servidores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64, verbose_name='Nome')),
                ('matricula', models.CharField(max_length=14, unique=True, verbose_name='Matrícula')),
                ('dt_inclusao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão')),
            ],
            options={
                'verbose_name': 'Meta-servidor',
                'verbose_name_plural': 'Meta-servidores (Lista de servidores do site da prefeitura)',
            },
        ),
    ]