# Generated by Django 4.2.11 on 2024-07-16 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0016_alter_pausas_execucao_do_chamado_user_fim_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pausas_execucao_do_chamado',
            name='motivo',
            field=models.TextField(blank=True, null=True, verbose_name='Motivo da pausa'),
        ),
    ]
