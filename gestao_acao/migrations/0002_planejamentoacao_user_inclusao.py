# Generated by Django 4.2.16 on 2025-04-07 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestao_acao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planejamentoacao',
            name='user_inclusao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acao_user_inclusao', to=settings.AUTH_USER_MODEL),
        ),
    ]
