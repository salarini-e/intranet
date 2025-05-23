# Generated by Django 4.2.20 on 2025-05-19 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('almoxarifado', '0003_alter_historicoitem_item_alter_historicoitem_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alocaitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.item'),
        ),
        migrations.AlterField(
            model_name='alocaitem',
            name='user',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='historicoitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.item'),
        ),
        migrations.AlterField(
            model_name='retiraitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.item'),
        ),
        migrations.AlterField(
            model_name='retiraitem',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
