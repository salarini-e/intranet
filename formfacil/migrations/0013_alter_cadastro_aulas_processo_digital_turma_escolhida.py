# Generated by Django 4.2.11 on 2024-09-03 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formfacil', '0012_cadastro_aulas_processo_digital_dt_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadastro_aulas_processo_digital',
            name='turma_escolhida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='formfacil.opcao_turmas', verbose_name='Selecione uma turma'),
        ),
    ]