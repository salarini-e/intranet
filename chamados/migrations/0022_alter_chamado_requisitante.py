# Generated by Django 4.2.11 on 2024-09-26 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instituicoes', '0013_alter_servidor_cpf'),
        ('chamados', '0021_alter_chamado_requisitante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='requisitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='instituicoes.servidor', verbose_name='Nome do servidor'),
        ),
    ]