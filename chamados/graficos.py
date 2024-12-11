# CHAMADOS POR SECRETARIA
from random import randint
from django.db.models import Count
from chamados.models import Chamado

DEFAULT_COLORS ={
    'impressora': 'black',
    'internet': 'yellow',
    'sistemas E&L': 'red',
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

def options_chamados_por_secretaria():
    return '''{
                responsive: true,
                plugins: {
                    datalabels: {
                        anchor: 'end', 
                        align: 'top',
                        color: 'black',
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
                            color: 'black', 
                        },
                        title: {
                            display: false,
                            text: 'Secretarias',
                            color: 'black'
                        }
                    },
                    y: {
                        ticks: { 
                            color: 'black', 
                        },
                        title: {
                            display: false,
                            text: 'Número de Chamados',
                            color: 'black'
                        },
                        beginAtZero: true
                    }
                }
            }
'''

def date_generic(titulo):
    return '''{
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: 'Exemplo',
                data: [10, 20, 15, 25, 30],
                backgroundColor: "'''+DEFAULT_COLORS[titulo]+'''",
                borderColor: "'''+DEFAULT_COLORS[titulo]+'''",
                borderWidth: 2
            }]
        };'''
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
    #             'color': 'black',
    #             'font': {
    #                 'weight': 'bold'
    #             },
    #             'formatter': 'value'
    #         },
    #         'title': {
    #             'display': True,
    #             'text': 'Exemplo',
    #             'color': 'black',
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
    #                 'color': 'black'
    #             },
    #             'title': {
    #                 'display': False,
    #                 'text': 'Secretarias',
    #                 'color': '#FFFFFF'
    #             }
    #         },
    #         'y': {
    #             'ticks': {
    #                 'color': 'black'
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
                    color: 'black', // Cor do texto
                    font: {
                        weight: 'bold'
                    },
                    formatter: (value) => {
                        return value; // Mostra o valor diretamente
                    }
                },               
                title: {
                            display: true,
                            text: "'''+titulo+'''",
                            color: 'black',
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
                            ticks: { color: 'black'},
                            title: {
                                display: false,
                                text: 'Secretarias',
                                color: '#FFFFFF'
                            }
                        },
                        y: {
                            ticks: { color: 'black' },
                            title: {
                                display: false,
                                text: 'Número de Chamados',
                                color: '#FFFFFF'
                            },
                            beginAtZero: true
                        }
                    }
        };'''