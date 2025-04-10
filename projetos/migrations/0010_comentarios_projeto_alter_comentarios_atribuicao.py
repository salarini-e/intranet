# Generated by Django 4.2.16 on 2025-02-19 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0009_anexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='projeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.projetos'),
        ),
        migrations.AlterField(
            model_name='comentarios',
            name='atribuicao',
            field=models.CharField(choices=[('p', 'Projeto'), ('t', 'Tarefa'), ('a', 'Atividade')], max_length=1),
        ),
    ]
