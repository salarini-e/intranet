# Generated by Django 4.2.11 on 2024-09-26 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instituicoes', '0012_alter_servidor_user_inclusao'),
        ('chamados', '0020_alter_chamado_requisitante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='requisitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='instituicoes.servidor', verbose_name='Nome'),
        ),
    ]