# Generated by Django 4.2.11 on 2024-09-17 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formfacil', '0013_alter_cadastro_aulas_processo_digital_turma_escolhida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadastro_aulas_processo_digital',
            name='matricula',
            field=models.CharField(blank=True, max_length=6, verbose_name='Matrícula'),
        ),
    ]