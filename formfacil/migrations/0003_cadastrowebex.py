# Generated by Django 4.2.11 on 2024-03-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formfacil', '0002_alter_formindicacaocomitepsp_observação'),
    ]

    operations = [
        migrations.CreateModel(
            name='CadastroWebex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secretaria', models.CharField(max_length=100)),
                ('setor', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=100, verbose_name='Nome completo')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('ramal', models.CharField(max_length=15, verbose_name='Telefone')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]