# Generated by Django 4.2.11 on 2024-08-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formfacil', '0005_alter_formsugestaosemananacionalcet2024_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CadastroEL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome completo')),
                ('matricula', models.CharField(max_length=10, verbose_name='Matrícula')),
                ('pdf_memorando', models.FileField(upload_to='uploads/', verbose_name='PDF do memorando')),
                ('sistemas', models.CharField(choices=[('pr', 'Protocolo'), ('tr', 'Tributário')], max_length=2, verbose_name='Quais sistemas você utiliza?')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
