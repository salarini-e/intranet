# Generated by Django 4.2.16 on 2025-06-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instituicoes', '0018_remove_dict_mapeamento_secretarias_nome_intranet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log_Nao_Encontrados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=14, unique=True, verbose_name='Matrícula')),
                ('nome', models.CharField(max_length=164, verbose_name='Nome')),
                ('secretaria', models.CharField(max_length=164, verbose_name='Secretaria')),
                ('erro', models.TextField(verbose_name='Erro')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
            ],
            options={
                'verbose_name': 'Log de Matrículas Não Encontradas',
                'verbose_name_plural': 'Logs de Matrículas Não Encontradas',
            },
        ),
    ]
