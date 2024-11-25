from chamados.models import Chamado, TipoChamado, Atendente
import calendar
from django.db.models import Count
from django.utils import timezone

from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models.functions import TruncMonth
from django.db import connection
from django.utils.timezone import now
from collections import defaultdict
from django.db.models import Count
from datetime import timedelta
import calendar

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


# def dados_evolucao_chamados_generic(value):


#     query = """
#         SELECT DATE_FORMAT(dt_inclusao, '%%Y-%%m-01') AS mes, COUNT(id) AS total
#         FROM chamados_chamado
#         WHERE tipo_id = (
#             SELECT id FROM chamados_tipochamado WHERE nome = %s
#         )
#         GROUP BY mes
#         ORDER BY mes;
#     """

#     with connection.cursor() as cursor:
#         cursor.execute(query, [value])
#         resultados = cursor.fetchall()

#     dados = {
#         "labels": [],
#         "values": []
#     }

#     for mes, total in resultados:
#         dados["labels"].append(mes)  # `mes` já está em formato de string
#         dados["values"].append(total)

#     return dados

def dados_evolucao_chamados_generic(value, periodo):    
    print(periodo)
    """
    Gera dados de evolução de chamados agrupados por dia, semana ou mês.

    :param value: O nome do tipo de chamado a ser filtrado.
    :param periodo: O período de agrupamento ('dia', 'semana', 'mes').
    :return: Um dicionário com labels e valores.
    """
    # Definindo o formato de agrupamento com base no período
    if periodo == 'dia':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%m-%%d')"  # Agrupamento diário
    elif periodo == 'semana':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%u')"  # Agrupamento semanal (ano-semana)
    elif periodo == 'mes':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%m')"  # Agrupamento mensal
    else:
        raise ValueError("Período inválido. Use 'dia', 'semana' ou 'mes'.")

    query = f"""
        SELECT {agrupamento} AS periodo, COUNT(id) AS total
        FROM chamados_chamado
        WHERE tipo_id = (
            SELECT id FROM chamados_tipochamado WHERE nome = %s
        )
        GROUP BY periodo
        ORDER BY periodo;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [value])
        resultados = cursor.fetchall()

    dados = {
        "labels": [],
        "values": []
    }

    for periodo_, total in resultados:
        if periodo == 'mes':
            ano, mes = periodo_.split("-")
            nome_mes = calendar.month_name[int(mes)] 
            dados["labels"].append(f"{nome_mes}")  
        elif periodo == 'dia':
            # Formatando a data no formato "dd/mm/yyyy"
            ano, mes, dia = periodo_.split("-")
            data_formatada = f"{int(dia):02d}/{int(mes):02d}/{ano}"
            dados["labels"].append(data_formatada)
        else:
            dados["labels"].append(periodo_)  # `periodo` já está em formato de string
        dados["values"].append(total)

    return dados

def dados_evolucao_chamados_internet(periodo):
    return dados_evolucao_chamados_generic('Internet', periodo)

def dados_evolucao_chamados_computadores(periodo):
    return dados_evolucao_chamados_generic('Computador', periodo)

def dados_evolucao_chamados_sistemas(periodo):
    return dados_evolucao_chamados_generic('Sistemas - E&L', periodo)

def dados_evolucao_chamados_impressora(periodo):
    return dados_evolucao_chamados_generic('Impressora', periodo)

def dados_evolucao_chamados_telefonia(periodo):
    return dados_evolucao_chamados_generic('Telefonia', periodo)



def dados_evolucao_atendimentos():
    # Definindo a data limite para os últimos 30 dias
    data_limite = now() - timedelta(days=30)

    # Query SQL ajustada para usar profissional_designado
    query = """
        SELECT 
            DATE(chamado.dt_fechamento) AS dia,
            atendente.nome_servidor AS atendente,
            COUNT(chamado.id) AS total
        FROM chamados_chamado AS chamado
        LEFT JOIN chamados_atendente AS atendente
            ON chamado.profissional_designado_id = atendente.id
        WHERE chamado.dt_fechamento >= %s AND chamado.dt_fechamento IS NOT NULL
        GROUP BY dia, atendente
        ORDER BY dia;
    """

    # Executar a query no banco de dados
    with connection.cursor() as cursor:
        cursor.execute(query, [data_limite])
        results = cursor.fetchall()

    # Estrutura para os dados
    dados = {
        "labels": [],
        "datasets": []
    }

    atendente_data = defaultdict(lambda: defaultdict(int))
    dias_set = set()

    # Processar os resultados da query
    for dia, atendente, total in results:
        dia_str = dia.strftime("%d %b")
        dias_set.add(dia_str)
        atendente_data[atendente or "Não definido"][dia_str] = total

    # Ordenar as datas
    dados["labels"] = sorted(dias_set)

    # Criar os datasets
    for atendente, dia_totais in atendente_data.items():
        dataset = {
            "label": atendente.split()[0],  # Usar apenas o primeiro nome
            "data": [dia_totais.get(dia, 0) for dia in dados["labels"]]
        }
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