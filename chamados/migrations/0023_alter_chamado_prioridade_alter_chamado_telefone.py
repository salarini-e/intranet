# Generated by Django 4.2.11 on 2024-10-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0022_alter_chamado_requisitante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='prioridade',
            field=models.CharField(choices=[('-', 'Não definida'), ('0', 'Baixa'), ('1', 'Média'), ('2', 'Alta')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='telefone',
            field=models.CharField(max_length=16, verbose_name='Qual telefone para contato?'),
        ),
    ]
