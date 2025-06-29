# CHAMADOS POR SECRETARIA
from random import randint
from django.db.models import Count
from chamados.models import Chamado
from django.db import connection
import calendar

from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

from django.utils.timezone import make_aware
from datetime import datetime, timedelta


DEFAULT_COLORS ={
    'impressora': 'white',
    'internet': 'yellow',
    'sistemas - E&L': 'red',
    'computador': 'blue',
    'telefonia': 'green'
}
def loadColors(qnt):
    colors = []
    for i in range(qnt):
        colors.append(f'rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, 0.8)')
    return colors

def date_chamados_por_secretaria():
    chamados = (
        Chamado.objects.values("secretaria__apelido")  # Agrupar pelos nomes das secretarias
        .annotate(total=Count("id"))  # Contar os chamados por secretaria
        .order_by("-total")  # Ordenar por número de chamados em ordem decrescente
    )
    cores = loadColors(len(chamados))

    data = {
        "labels": [],
        "datasets": [{
            'label': 'Total de chamados',
            'data': [], 
            'backgroundColor': cores,
            'borderColor': cores,
            'borderWidth': 1

        }]
    }

    for chamado in chamados:
        data["labels"].append(chamado["secretaria__apelido"])  # Nome da secretaria
        data["datasets"][0]["data"].append(chamado["total"])  # Total de chamados

    return data

# def date_chamados_por_atendente():
#     chamados = (
#         Chamado.objects.values("profissional_designado__nome_servidor")  # Agrupar pelos nomes das secretarias
#         .annotate(total=Count("id"))  # Contar os chamados por secretaria
#         .order_by("-total")  # Ordenar por número de chamados em ordem decrescente
#     )
#     cores = loadColors(len(chamados))

#     data = {
#         "labels": [],
#         "datasets": [{
#             'label': 'Total de chamados',
#             'data': [], 
#             'backgroundColor': cores,
#             'borderColor': cores,
#             'borderWidth': 1

#         }]
#     }

#     for chamado in chamados:
#         nome = chamado["profissional_designado__nome_servidor"].split()[0] if chamado["profissional_designado__nome_servidor"] else "Sem atendente"
#         data["labels"].append(nome)  # Nome da secretaria
#         data["datasets"][0]["data"].append(chamado["total"])  # Total de chamados
#     # print(data)
#     return data

from django.db.models import Count, Q

def date_chamados_por_atendente():
    # Contando chamados atendidos e pendentes
    chamados = (
        Chamado.objects
        .filter(profissional_designado__ativo=True)
        .values("profissional_designado__nome_servidor")  # Agrupar pelos nomes dos atendentes
        .annotate(
            total_atendidos=Count("id", filter=Q(status__in=[4])),   
            total_pendentes=Count("id", filter=~Q(status__in=[4, 5, 6])),  
        )
        .order_by("-total_atendidos")  # Ordenar por chamados atendidos em ordem decrescente
    )

    cores = loadColors(len(chamados))

    data = {
        "labels": [],  # Nomes dos atendentes
        "datasets": [
            {
                'label': 'Chamados Atendidos',
                'data': [],
                'backgroundColor': cores,  # Cores para os chamados atendidos
                'borderColor': cores,
                'borderWidth': 1
            },
            {
                'label': 'Chamados Pendentes',
                'data': [],
                'backgroundColor': '#FF5733',  # Cores para os chamados pendentes
                'borderColor': '#FF5733',
                'borderWidth': 1
            }
        ]
    }

    for chamado in chamados:
        nome = chamado["profissional_designado__nome_servidor"].split()[0] if chamado["profissional_designado__nome_servidor"] else "Sem atendente"
        data["labels"].append(nome)  # Nome do atendente
        data["datasets"][0]["data"].append(chamado["total_atendidos"])  # Chamados atendidos
        data["datasets"][1]["data"].append(chamado["total_pendentes"])  # Chamados pendentes

    return data

def date_chamados_por_mes():
    # Certifique-se de que `inicio_periodo` está no formato adequado
    inicio_periodo = make_aware(datetime.now() - timedelta(days=365))
    
    # Corrigido: Remover id do SELECT e usar cursor
    sql = '''
        SELECT
            DATE_FORMAT(dt_inclusao, '%%Y-%%m-01') AS mes,
            COUNT(id) AS total
        FROM chamados_chamado
        WHERE dt_inclusao >= %s
        GROUP BY mes
        ORDER BY mes ASC
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [inicio_periodo])
        result = cursor.fetchall()

    cores = loadColors(len(result))
    data = {
        "labels": [],
        "datasets": [{
            'label': 'Total de chamados',
            'data': [], 
            'backgroundColor': cores,
            'borderColor': cores,
            'borderWidth': 1

        }]
    }
    for row in result:
        mes = datetime.strptime(row[0], "%Y-%m-%d")
        mes_formatado = mes.strftime("%B de %Y")
        data["labels"].append(mes_formatado.capitalize())
        data["datasets"][0]["data"].append(row[1])
    # print(data)
    return data

from django.utils import timezone

def data_generic(titulo, periodo='dia'):    
    """
    Gera dados de evolução de chamados agrupados por dia, semana ou mês.

    :param titulo: O nome do tipo de chamado a ser filtrado.
    :param periodo: O período de agrupamento ('dia', 'semana', 'mes').
    :return: Um dicionário com labels e valores.
    """

    data = {
        "labels": [],
        "datasets": [{
            'label': 'Total de chamados',
            'data': [], 
            'backgroundColor': DEFAULT_COLORS[titulo],
            'borderColor': DEFAULT_COLORS[titulo],
            'borderWidth': 2,
        }]
    }

    # Definindo o formato de agrupamento com base no período
    if periodo == 'dia':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%m-%%d')"  # Agrupamento diário
    elif periodo == 'semana':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%u')"  # Agrupamento semanal (ano-semana)
    elif periodo == 'mes':
        agrupamento = "DATE_FORMAT(dt_inclusao, '%%Y-%%m')"  # Agrupamento mensal
    else:
        raise ValueError("Período inválido. Use 'dia', 'semana' ou 'mes'.")

    # Filtro de data para os últimos 30 dias
    data_inicio = timezone.now() - timedelta(days=30)

    query = f"""
        SELECT {agrupamento} AS periodo, COUNT(id) AS total
        FROM chamados_chamado
        WHERE tipo_id = (
            SELECT id FROM chamados_tipochamado WHERE nome = %s
        )
        AND dt_inclusao >= %s
        GROUP BY periodo
        ORDER BY periodo;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [titulo, data_inicio])
        resultados = cursor.fetchall()

    for periodo_, total in resultados:
        if periodo == 'mes':
            ano, mes = periodo_.split("-")
            nome_mes = calendar.month_name[int(mes)] 
            data["labels"].append(f"{nome_mes}")  
        elif periodo == 'dia':
            ano, mes, dia = periodo_.split("-")
            data_formatada = f"{int(dia):02d}/{int(mes):02d}"
            data["labels"].append(data_formatada)
        else:
            data["labels"].append(periodo_)
        data['datasets'][0]["data"].append(total)

    return data

def data_generic_bar_semanal(titulo):
    """
    Gera dados para gráfico de barras agrupados por semana (segunda a domingo),
    considerando as últimas 10 semanas (incluindo a atual).
    """
    from django.utils import timezone
    import calendar

    data = {
        "labels": [],
        "datasets": [{
            'label': 'Total de chamados',
            'data': [],
            'backgroundColor': DEFAULT_COLORS[titulo],
            'borderColor': DEFAULT_COLORS[titulo],
            'borderWidth': 2,
        }]
    }

    # Calcular a data da segunda-feira da semana atual
    hoje = timezone.now().date()
    weekday = hoje.weekday()  # 0 = segunda-feira
    segunda_atual = hoje - timedelta(days=weekday)

    # Calcular a data da segunda-feira de 11 semanas atrás (total 10 semanas)
    segunda_inicio = segunda_atual - timedelta(weeks=11)

    # Gerar lista de segundas-feiras (início de cada semana)
    semanas = [segunda_inicio + timedelta(weeks=i) for i in range(10)]

    # Buscar os dados do banco agrupando por semana (segunda-feira)
    agrupamento = "DATE_FORMAT(DATE_SUB(dt_inclusao, INTERVAL(WEEKDAY(dt_inclusao)) DAY), '%%Y-%%m-%%d')"
    data_inicio = segunda_inicio

    query = f"""
        SELECT {agrupamento} AS semana_inicio, COUNT(id) AS total
        FROM chamados_chamado
        WHERE tipo_id = (
            SELECT id FROM chamados_tipochamado WHERE nome = %s
        )
        AND dt_inclusao >= %s
        GROUP BY semana_inicio
        ORDER BY semana_inicio;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [titulo, data_inicio])
        resultados = cursor.fetchall()
        # Corrige: converte a chave para str, não para int
        resultados_dict = {str(row[0]): row[1] for row in resultados}

    # Montar os labels e os dados, garantindo 0 para semanas sem chamados
    for segunda in semanas:
        label = segunda.strftime("%d/%m/%Y")
        chave = segunda.strftime("%Y-%m-%d")
        data["labels"].append(label)
        data['datasets'][0]["data"].append(resultados_dict.get(chave, 0))

    return data

def options_chamados_por_secretaria():
    return '''{
                responsive: true,
                plugins: {
                    datalabels: {
                        anchor: 'end', 
                        align: 'top',
                        color: 'white',
                    },
                    title: {
                        display: false,
                        text: 'Chamados por Secretaria',
                        color: '#FFFFFF',
                        font: {
                            size: 8
                        }
                       },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Total: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Secretarias',
                            color: 'white'
                        }
                    },
                    y: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Número de Chamados',
                            color: 'white'
                        },
                        beginAtZero: true
                    }
                }
            }
'''
# def options_chamados_por_atendente():
#     return '''{
#                 responsive: true,
#                 plugins: {
#                     datalabels: {
#                         anchor: 'end', 
#                         align: 'top',
#                         color: 'white',
#                     },
#                     title: {
#                         display: false,
#                         text: 'Chamados por Atendentes',
#                         color: '#FFFFFF',
#                         font: {
#                             size: 8
#                         }
#                        },
#                     legend: {
#                         display: false
#                     },
#                     tooltip: {
#                         callbacks: {
#                             label: function(context) {
#                                 return `Total: ${context.raw}`;
#                             }
#                         }
#                     }
#                 },
#                 scales: {
#                     x: {
#                         ticks: { 
#                             color: 'white', 
#                         },
#                         title: {
#                             display: false,
#                             text: 'Atendentes',
#                             color: 'white'
#                         }
#                     },
#                     y: {
#                         ticks: { 
#                             color: 'white', 
#                         },
#                         title: {
#                             display: false,
#                             text: 'Número de Chamados',
#                             color: 'white'
#                         },
#                         beginAtZero: true
#                     }
#                 }
#             }
# '''
def options_chamados_por_atendente():
    return '''{
                responsive: true,
                plugins: {
                    datalabels: {
                        anchor: 'end', 
                        align: 'top',
                        color: 'white',
                    },
                    title: {
                        display: false,
                        text: 'Chamados por Atendentes',
                        color: '#FFFFFF',
                        font: {
                            size: 8
                        }
                    },
                    legend: {
                        display: true
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Total: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Atendentes',
                            color: 'white'
                        }
                    },
                    y: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Número de Chamados',
                            color: 'white'
                        },
                        beginAtZero: true
                    }
                },
                barThickness: 30,  // Ajuste para garantir que as barras fiquem lado a lado
                indexAxis: 'x'  // Organizar as barras horizontalmente
            }
'''

def options_chamados_por_mes():
    return '''{
                responsive: true,
                plugins: {
                    datalabels: {
                        anchor: 'end', 
                        align: 'top',
                        color: 'white',
                    },
                    title: {
                        display: false,
                        text: 'Chamados por Mês',
                        color: '#FFFFFF',
                        font: {
                            size: 8
                        }
                       },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Total: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Mês',
                            color: 'white'
                        }
                    },
                    y: {
                        ticks: { 
                            color: 'white', 
                        },
                        title: {
                            display: false,
                            text: 'Número de Chamados',
                            color: 'white'
                        },
                        beginAtZero: true
                    }
                }
            }
'''

# def data_generic(titulo):
#     return '''{
#             labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
#             datasets: [{
#                 label: 'Exemplo',
#                 data: [10, 20, 15, 25, 30],
#                 backgroundColor: "'''+DEFAULT_COLORS[titulo]+'''",
#                 borderColor: "'''+DEFAULT_COLORS[titulo]+'''",
#                 borderWidth: 2
#             }]
#         };'''
def options_generic(titulo):
    # options = {
    #     'responsive': True,
    #     'plugins': {
    #         'legend': {
    #             'display': False
    #         },
    #         'datalabels': {
    #             'anchor': 'end',
    #             'align': 'end',
    #             'color': 'white',
    #             'font': {
    #                 'weight': 'bold'
    #             },
    #             'formatter': 'value'
    #         },
    #         'title': {
    #             'display': True,
    #             'text': 'Exemplo',
    #             'color': 'white',
    #             'font': {
    #                 'size': 20
    #             }
    #         },
    #         'legend': {
    #             'display': False
    #         },
    #         'tooltip': {
    #             'callbacks': {
    #                 'label': 'Total: ${context.raw}'
    #             }
    #         }
    #     },
    #     'scales': {
    #         'x': {
    #             'ticks': {
    #                 'color': 'white'
    #             },
    #             'title': {
    #                 'display': False,
    #                 'text': 'Secretarias',
    #                 'color': '#FFFFFF'
    #             }
    #         },
    #         'y': {
    #             'ticks': {
    #                 'color': 'white'
    #             },
    #             'title': {
    #                 'display': False,
    #                 'text': 'Número de Chamados',
    #                 'color': '#FFFFFF'
    #             },
    #             'beginAtZero': True
    #         }
    #     }        
    # }
    return '''{
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                datalabels: {
                    anchor: 'end', // Onde o texto será fixado
                    align: 'end',  // Alinhamento do texto
                    color: 'white', // Cor do texto
                    font: {
                        weight: 'bold'
                    },
                    formatter: (value) => {
                        return value; // Mostra o valor diretamente
                    }
                },               
                title: {
                            display: false  ,
                            text: "'''+titulo+'''",
                            color: 'white',
                            font: {
                                size: 20
                            }                            
                        }, 
                legend: {
                            display: false // Desativa a legenda
                        },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Total: ${context.raw}`;
                        }
                    }
                }
            },
            scales: {
                        x: {
                            ticks: { color: 'white'},
                            title: {
                                display: false,
                                text: 'Secretarias',
                                color: '#FFFFFF'
                            }
                        },
                        y: {
                            ticks: { color: 'white' },
                            title: {
                                display: false,
                                text: 'Número de Chamados',
                                color: '#FFFFFF'
                            },
                            beginAtZero: true
                        }
                    }
        };'''