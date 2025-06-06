# Generated by Django 4.2.16 on 2025-06-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0029_alter_demandas_prioridade_alter_demandas_referencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandas',
            name='prioridade',
            field=models.IntegerField(choices=[(2, 'Importante'), (0, 'Regular'), (3, 'Urgente'), (1, 'Média')], default=0),
        ),
        migrations.AlterField(
            model_name='demandas',
            name='referencia',
            field=models.CharField(choices=[('a', 'Gestão de Projetos'), ('n', 'Nenhuma'), ('t', 'Gestão de Projetos'), ('p', 'Ação planejada')], default='n', max_length=1),
        ),
    ]
