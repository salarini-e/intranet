# Generated by Django 4.2.16 on 2024-12-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_noticias'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticias',
            name='link',
            field=models.CharField(default='#', max_length=200),
        ),
        migrations.AddField(
            model_name='noticias',
            name='resumo',
            field=models.TextField(default=''),
        ),
    ]
