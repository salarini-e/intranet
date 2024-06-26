# Generated by Django 5.0.3 on 2024-03-20 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instituicoes', '0003_secretaria_apelido_secretaria_user_inclusao_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_servidor', models.CharField(blank=True, max_length=64, null=True, verbose_name='Nome de usuário')),
                ('dt_inclusao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('servidor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='instituicoes.servidor', verbose_name='Servidor')),
                ('user_inclusao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de inclusão')),
            ],
            options={
                'verbose_name': 'Atendente',
                'verbose_name_plural': 'Atendentes',
            },
        ),
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=14, verbose_name='Telefone')),
                ('assunto', models.CharField(max_length=64, verbose_name='Assunto')),
                ('prioridade', models.CharField(choices=[('0', 'Baixa'), ('1', 'Média'), ('2', 'Alta')], default='0', max_length=1)),
                ('status', models.CharField(choices=[('0', 'Aberto'), ('2', 'Em atendimento'), ('1', 'Pendente'), ('3', 'Fechado'), ('4', 'Finalizado')], default='0', max_length=1)),
                ('descricao', models.TextField(default='')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('dt_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de ultima atualização')),
                ('dt_execucao', models.DateField(verbose_name='Data da execução do chamado')),
                ('dt_fechamento', models.DateTimeField(verbose_name='Data do fechamaneto do chamado')),
                ('n_protocolo', models.CharField(max_length=14, null=True, verbose_name='Número de protocolo')),
                ('anexo', models.FileField(blank=True, default=None, null=True, upload_to='chamados/anexos/')),
                ('hash', models.CharField(max_length=64)),
                ('atendente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chamados_atendente', to='chamados.atendente', verbose_name='Atendente')),
                ('profissional_designado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profissional_designado_chamados', to='chamados.atendente', verbose_name='Profissional designado')),
                ('requisitante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisitante_chamados', to='instituicoes.servidor', verbose_name='Servidor')),
                ('setor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='instituicoes.setor', verbose_name='Setor')),
                ('user_atualizacao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_atualizacao_chamados', to='instituicoes.servidor', verbose_name='Usuário da ultima atualização')),
                ('user_inclusao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_inclusao_chamados', to='instituicoes.servidor', verbose_name='Usuário que cadastrou')),
            ],
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
                ('anexo', models.FileField(blank=True, default=None, null=True, upload_to='chamados/anexos/')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('confidencial', models.BooleanField(default=False, verbose_name='Confidencial')),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chamados.chamado', verbose_name='Chamado')),
                ('servidor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servidor_mensagens', to='instituicoes.servidor', verbose_name='Servidor')),
                ('user_inclusao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_inclusao_mensagens', to='instituicoes.servidor', verbose_name='Usuário de inclusão')),
            ],
        ),
        migrations.CreateModel(
            name='OSImpressora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_serie', models.CharField(max_length=64, verbose_name='Número de série')),
                ('contador', models.IntegerField(verbose_name='Contador')),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chamados.chamado', verbose_name='Chamado')),
            ],
        ),
        migrations.CreateModel(
            name='OSInternet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nofcip', models.CharField(max_length=64, verbose_name='Nofcip')),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chamados.chamado', verbose_name='Chamado')),
            ],
        ),
        migrations.CreateModel(
            name='OSSistemas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sistema', models.CharField(max_length=64, verbose_name='Sistema')),
                ('versao', models.CharField(max_length=64, verbose_name='Versão')),
                ('chamado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chamados.chamado', verbose_name='Chamado')),
            ],
        ),
        migrations.CreateModel(
            name='TipoChamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=164, verbose_name='Nome')),
                ('sigla', models.CharField(max_length=8, verbose_name='Sigla')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('dt_inclusao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('user_inclusao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de inclusão')),
            ],
            options={
                'verbose_name': 'Tipo de Chamado',
                'verbose_name_plural': 'Tipos de Chamados',
            },
        ),
        migrations.AddField(
            model_name='chamado',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chamados.tipochamado', verbose_name='Tipo chamado'),
        ),
        migrations.AddField(
            model_name='atendente',
            name='tipo',
            field=models.ManyToManyField(to='chamados.tipochamado'),
        ),
    ]
