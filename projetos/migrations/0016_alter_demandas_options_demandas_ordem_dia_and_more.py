# Generated by Django 4.2.16 on 2025-04-01 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0015_demandas_data_prevista_execucao_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demandas',
            options={'ordering': ['ordem_dia', 'data_prevista_execucao', 'nome'], 'verbose_name': 'Demanda', 'verbose_name_plural': 'Demandas'},
        ),
        migrations.AddField(
            model_name='demandas',
            name='ordem_dia',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ordem do dia'),
        ),
        migrations.AlterField(
            model_name='demandas',
            name='prioridade',
            field=models.IntegerField(choices=[(3, 'Urgente'), (2, 'Importante'), (1, 'Média'), (0, 'Regular')], default=0),
        ),
        migrations.AlterField(
            model_name='demandas',
            name='referencia',
            field=models.CharField(choices=[('n', 'Nenhuma'), ('a', 'Atividade'), ('t', 'Tarefa')], default='n', max_length=1),
        ),
        migrations.AlterField(
            model_name='demandas',
            name='rotina',
            field=models.BooleanField(default=False, verbose_name='É uma rotina?'),
        ),
    ]
