# Generated by Django 4.2.16 on 2025-01-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projetos',
            name='orcamento',
        ),
        migrations.AlterField(
            model_name='projetos',
            name='status',
            field=models.CharField(choices=[('C', 'Planejamento'), ('E', 'Em andamento'), ('F', 'Finalizado'), ('P', 'Parado')], default='C', max_length=1),
        ),
    ]
