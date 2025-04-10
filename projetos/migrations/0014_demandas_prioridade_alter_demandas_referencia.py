# Generated by Django 4.2.16 on 2025-03-31 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0013_demandas'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandas',
            name='prioridade',
            field=models.IntegerField(choices=[(1, 'Média'), (3, 'Urgente'), (0, 'Regular'), (2, 'Importante')], default=0),
        ),
        migrations.AlterField(
            model_name='demandas',
            name='referencia',
            field=models.CharField(choices=[('t', 'Tarefa'), ('n', 'Nenhuma'), ('a', 'Atividade')], default='n', max_length=1),
        ),
    ]
