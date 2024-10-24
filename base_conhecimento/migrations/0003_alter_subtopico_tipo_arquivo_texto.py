# Generated by Django 4.2.11 on 2024-09-04 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_conhecimento', '0002_topico_ativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopico',
            name='tipo',
            field=models.CharField(choices=[('ytb', 'youtube'), ('pdf', 'pdf'), ('txt', 'texto')], max_length=3, verbose_name='Tipo'),
        ),
        migrations.CreateModel(
            name='Arquivo_Texto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto')),
                ('subtopico', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base_conhecimento.subtopico', verbose_name='Subtópico Associado')),
            ],
        ),
    ]
