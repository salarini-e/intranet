# Generated by Django 4.2.11 on 2024-08-27 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formfacil', '0010_opcao_turmas_cadastro_aulas_processo_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcao_turmas',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Opcao de turma ainda aberta?'),
        ),
        migrations.AlterField(
            model_name='cadastro_aulas_processo_digital',
            name='secretaria',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='cadastro_aulas_processo_digital',
            name='setor',
            field=models.CharField(max_length=250),
        ),
    ]
