# Generated by Django 4.2.11 on 2024-04-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0010_ostelefonia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendente',
            name='nivel',
            field=models.CharField(choices=[('0', 'Nível 1 - Help Desk'), ('1', 'Nível 2 - Suporte Técnico'), ('2', 'Nível 3 - Administração')], default='0', max_length=1),
        ),
    ]
