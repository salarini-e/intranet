# Generated by Django 4.2.16 on 2024-12-07 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrousell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('imagem', models.ImageField(upload_to='noticias/carrousell/')),
                ('alt', models.CharField(max_length=100)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]