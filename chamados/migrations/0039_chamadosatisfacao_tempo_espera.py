# Generated by Django 4.2.16 on 2025-01-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0038_alter_chamadosatisfacao_resolucao'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamadosatisfacao',
            name='tempo_espera',
            field=models.CharField(choices=[('0', 'Ruim'), ('1', 'Regular'), ('2', 'Bom'), ('3', 'Ótimo'), ('4', 'Excelente')], max_length=1, null=True, verbose_name='Como você avalia o tempo de espera para o atendimento?'),
        ),
    ]
