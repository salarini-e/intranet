# Generated by Django 4.2.16 on 2025-02-13 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0006_grupo_responsavel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fases',
            unique_together=set(),
        ),
    ]
