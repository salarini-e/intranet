# Generated by Django 4.2.11 on 2024-09-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_conhecimento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topico',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
