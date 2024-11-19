from chamados.models import Chamado, TipoChamado, Atendente
import calendar
from django.db.models import Count
from django.utils import timezone

from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models.functions import TruncMonth
from django.db import connection

def dados_total_atendimentos_realizados():
    meses = [calendar.month_name[i] for i in range(1, 13)]
    atendidos = [0] * 12
    nao_atendidos = [0] * 12

    chamados = Chamado.objects.all()
    for chamado in chamados:
        mes = chamado.dt_inclusao.month - 1
        if chamado.status in ['3', '4']:
            atendidos[mes] += 1
        else:
            nao_atendidos[mes] += 1

    return {
        "labels": meses,
        "datasets": [
            {"label": "Atendidos", "data": atendidos, "backgroundColor": "blue"},
            {"label": "Não Atendidos", "data": nao_atendidos, "backgroundColor": "red"}
        ]
    }

def dados_percentual_chamados_por_servico():
    chamados_por_servico = TipoChamado.objects.all().annotate(total_chamados=Count('chamado'))

    # Preparar os dados
    dados = {
        "labels": [],
        "values": [],
        "colors": ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD', '#1F618D', '#D35400', '#7D3C98']
    }

    total_chamados = sum([tipo.total_chamados for tipo in chamados_por_servico])

    for tipo in chamados_por_servico:
        dados["labels"].append(tipo.nome)
        percentual = (tipo.total_chamados / total_chamados) * 100 if total_chamados > 0 else 0
        dados["values"].append(percentual)

    # Garantir que as cores correspondam ao número de serviços
    if len(dados["colors"]) < len(dados["labels"]):
        dados["colors"] = dados["colors"] * (len(dados["labels"]) // len(dados["colors"])) + dados["colors"][:len(dados["labels"]) % len(dados["colors"])]

    return dados


def dados_evolucao_chamados_generic(value):


    query = """
        SELECT DATE_FORMAT(dt_inclusao, '%%Y-%%m-01') AS mes, COUNT(id) AS total
        FROM chamados_chamado
        WHERE tipo_id = (
            SELECT id FROM chamados_tipochamado WHERE nome = %s
        )
        GROUP BY mes
        ORDER BY mes;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [value])
        resultados = cursor.fetchall()

    dados = {
        "labels": [],
        "values": []
    }

    for mes, total in resultados:
        dados["labels"].append(mes)  # `mes` já está em formato de string
        dados["values"].append(total)

    return dados

def dados_evolucao_chamados_internet():
    return dados_evolucao_chamados_generic('Internet')

def dados_evolucao_chamados_computadores():
    return dados_evolucao_chamados_generic('Computador')

def dados_evolucao_chamados_sistemas():
    return dados_evolucao_chamados_generic('Sistemas - E&L')

def dados_evolucao_chamados_impressora():
    return dados_evolucao_chamados_generic('Impressora')

def dados_evolucao_chamados_telefonia():
    return dados_evolucao_chamados_generic('Telefonia')

def dados_evolucao_atendimentos():
    # Definindo a data limite para os últimos 30 dias
    data_limite = timezone.now() - timezone.timedelta(days=30)

    atendimentos = (
        Chamado.objects.filter(dt_execucao__gte=data_limite)
        .annotate(dia=TruncDate('dt_fechamento'))  # Truncando para o dia
        .values('dia', 'atendente__nome_servidor')  # Agrupando por data e atendente
        .annotate(total=Count('id'))  # Contando o número de atendimentos por dia
        .order_by('dia')  # Ordenando por data
    )

    dados = {
        "labels": [],  # Datas
        "datasets": []  # Atendentes
    }

    # Organizar os dados
    atendentes = set()  # Para armazenar os atendentes
    for atendimento in atendimentos:
        dados["labels"].append(atendimento["dia"].strftime("%d %b"))
        atendentes.add(atendimento["atendente__nome_servidor"])

    # Para cada atendente, criar um dataset com os dados
    for atendente in atendentes:
        dataset = {
            "label": atendente,
            "data": []
        }
        for atendimento in atendimentos:
            if atendimento["atendente__nome_servidor"] == atendente:
                dataset["data"].append(atendimento["total"])
            else:
                dataset["data"].append(0)  # Caso o atendente não tenha atendido naquele dia
        dados["datasets"].append(dataset)

    return dados



def dados_chamados_por_secretaria():
    chamados = (
        Chamado.objects.values("secretaria__apelido")  # Agrupar pelos nomes das secretarias
        .annotate(total=Count("id"))  # Contar os chamados por secretaria
        .order_by("-total")  # Ordenar por número de chamados em ordem decrescente
    )

    dados = {
        "labels": [],
        "values": []
    }

    for chamado in chamados:
        dados["labels"].append(chamado["secretaria__apelido"])  # Nome da secretaria
        dados["values"].append(chamado["total"])  # Total de chamados

    return dados