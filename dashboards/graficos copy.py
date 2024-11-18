from chamados.models import Chamado, TipoChamado
import calendar
from plotly import graph_objects as go
from plotly import io as pio
import plotly.express as px
import pandas as pd
from django.db.models import Count, Q


def graf_total_atendimentos_realizados():
    # Listar os meses do ano
    meses = [calendar.month_name[i] for i in range(1, 13)]
    
    # Inicializar as listas para armazenar os dados de chamados atendidos e não atendidos
    atendidos = [0] * 12
    nao_atendidos = [0] * 12

    # Consultar os chamados agrupados por mês
    chamados = Chamado.objects.all()
    
    for chamado in chamados:
        # Verificar o mês em que o chamado foi criado (considerando a data de inclusão)
        mes = chamado.dt_inclusao.month - 1  # Ajustar para o índice da lista (0-11)
        
        # Contabilizar os chamados atendidos (status '4' ou '3' ou qualquer outro status finalizado)
        if chamado.status in ['3', '4']:  # Aqui você pode ajustar os status finais de acordo com sua necessidade
            atendidos[mes] += 1
        else:  # Chamados que ainda estão pendentes ou em andamento
            nao_atendidos[mes] += 1

    # Criar o gráfico
    fig = go.Figure(data=[
        go.Bar(name='Atendidos', x=meses, y=atendidos, marker_color='blue'),
        go.Bar(name='Não Atendidos', x=meses, y=nao_atendidos, marker_color='red')
    ])

    # Atualizar o layout do gráfico
    fig.update_layout(
        title="Total de Atendimentos de Chamados por Mês",
        xaxis_title="Mês",
        yaxis_title="Total de Chamados",
        barmode='stack',
        plot_bgcolor="rgb(28, 28, 28)",  # Fundo das áreas de plotagem
        paper_bgcolor="rgb(28, 28, 28)",  # Fundo da área externa do gráfico
        font=dict(color="white")  # Cor das fontes do gráfico para branco
    )

    # Converter para HTML
    grafico_html = pio.to_html(fig, full_html=False)
    
    return grafico_html


def graf_percentual_chamados_por_servico():
    # Criando uma lista de cores personalizadas para as barras
    cores = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD', '#1F618D', '#D35400', '#7D3C98']
    
    # Recuperando dados de todos os tipos de chamados com a contagem de chamados para cada tipo
    chamados_por_servico = TipoChamado.objects.all().annotate(total_chamados=Count('chamado'))

    # Preparando listas para armazenar os valores do gráfico
    tipos_nome = []
    percentuais = []
    cores_usadas = []

    # Calculando o total de chamados
    total_chamados = sum([tipo.total_chamados for tipo in chamados_por_servico])

    # Garantir que a lista de cores tenha o mesmo tamanho que o número de tipos de serviços
    if len(cores) < len(chamados_por_servico):
        cores = cores * (len(chamados_por_servico) // len(cores)) + cores[:len(chamados_por_servico) % len(cores)]

    # Loop para calcular percentuais e preencher as listas
    for i, tipo in enumerate(chamados_por_servico):
        tipos_nome.append(tipo.nome)  # Nome do tipo de chamado
        percentual = (tipo.total_chamados / total_chamados) * 100
        percentuais.append(percentual)  # Percentual de chamados por tipo
        cores_usadas.append(cores[i])  # Atribuindo uma cor para cada barra

    # Criando o gráfico de barras com as informações calculadas
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=tipos_nome,  # Tipos de serviços
        y=percentuais,  # Percentuais de chamados
        name="Percentual de Chamados",
        marker_color=cores_usadas  # Cores específicas para cada barra
    ))

    # Adicionando título e rótulos
    fig.update_layout(
        title="Percentual de Chamados por Tipo de Serviço",
        xaxis_title="Tipo de Serviço",
        yaxis_title="Percentual (%)",
        template="plotly_white",
        height=600,
        showlegend=False,
        plot_bgcolor="rgb(28, 28, 28)",  # Fundo das áreas de plotagem
        paper_bgcolor="rgb(28, 28, 28)",  # Fundo da área externa do gráfico
        font=dict(color="white"),  # Cor das fontes do gráfico para branco
        xaxis=dict(
            tickmode='array',
            tickvals=tipos_nome,
            ticktext=tipos_nome  # Exibindo corretamente os nomes dos tipos no eixo X
        ),
    )
    
    # Convertendo o gráfico para HTML
    grafico_html = fig.to_html(full_html=False)
    
    return grafico_html


def graf_evolucao_chamados_por_tipo():
    # Consultando os dados no banco de dados (quantidade de chamados por tipo e mês)
    chamados_por_mes_tipo = Chamado.objects.values(
        'tipo__nome', 
        'dt_inclusao__month'
    ).annotate(total_chamados=Count('id'))
    
    # Convertendo para DataFrame para facilitar a manipulação dos dados
    df = pd.DataFrame(chamados_por_mes_tipo)

    # Mapeando os meses para nomes
    df['month_name'] = df['dt_inclusao__month'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })

    # Calculando o total de chamados por mês
    total_chamados_por_mes = df.groupby('dt_inclusao__month')['total_chamados'].sum()

    # Preparando os dados para o gráfico
    fig = go.Figure()

    # Obtendo a lista de tipos de serviço
    tipos_servico = df['tipo__nome'].unique()

    # Adicionando uma linha para cada tipo de serviço
    for tipo in tipos_servico:
        # Filtrando os dados para cada tipo de serviço
        dados_tipo = df[df['tipo__nome'] == tipo]

        # Preenchendo os valores de cada mês (se houver mês sem chamados, será tratado)
        chamados_por_mes = dados_tipo.groupby('dt_inclusao__month')['total_chamados'].sum().reindex(range(1, 13), fill_value=0)

        # Calculando o percentual de chamados para cada tipo de serviço em relação ao total de chamados
        percentual_por_mes = (chamados_por_mes / total_chamados_por_mes) * 100

        # Adicionando a linha ao gráfico
        fig.add_trace(go.Scatter(
            x=percentual_por_mes.index, 
            y=percentual_por_mes.values,
            mode='lines+markers',
            name=tipo
        ))

    # Adicionando título e rótulos ao gráfico
    fig.update_layout(
        title="Percentual dos Chamados por Tipo de Serviço",
        xaxis_title="Mês",
        yaxis_title="Percentual (%)",
        xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
        template="plotly_dark",  # Usando o tema escuro
        height=600
    )
    
    # Convertendo o gráfico para HTML
    grafico_html = fig.to_html(full_html=False)
    
    return grafico_html


def graf_percentual_chamados_por_secretaria():
    # Consultando os dados no banco de dados (quantidade de chamados por secretaria e mês)
    chamados_por_mes_secretaria = Chamado.objects.values(
        'secretaria__nome', 
        'dt_inclusao__month'
    ).annotate(total_chamados=Count('id'))
    
    # Convertendo para DataFrame para facilitar a manipulação dos dados
    df = pd.DataFrame(chamados_por_mes_secretaria)

    # Mapeando os meses para nomes
    df['month_name'] = df['dt_inclusao__month'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })

    # Calculando o total de chamados por mês
    total_chamados_por_mes = df.groupby('dt_inclusao__month')['total_chamados'].sum()

    # Preparando os dados para o gráfico
    fig = go.Figure()

    # Obtendo a lista de secretarias
    secretarias = df['secretaria__nome'].unique()

    # Adicionando uma linha para cada secretaria
    for secretaria in secretarias:
        # Filtrando os dados para cada secretaria
        dados_secretaria = df[df['secretaria__nome'] == secretaria]

        # Preenchendo os valores de cada mês (se houver mês sem chamados, será tratado)
        chamados_por_mes = dados_secretaria.groupby('dt_inclusao__month')['total_chamados'].sum().reindex(range(1, 13), fill_value=0)

        # Calculando o percentual de chamados para cada secretaria em relação ao total de chamados
        percentual_por_mes = (chamados_por_mes / total_chamados_por_mes) * 100

        # Adicionando a linha ao gráfico
        fig.add_trace(go.Scatter(
            x=percentual_por_mes.index, 
            y=percentual_por_mes.values,
            mode='lines+markers',
            name=secretaria
        ))

    # Adicionando título e rótulos ao gráfico
    fig.update_layout(
        title="Percentual dos Chamados por Secretaria",
        xaxis_title="Mês",
        yaxis_title="Percentual (%)",
        xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
        template="plotly_dark",  # Usando o tema escuro
        height=600
    )
    
    # Convertendo o gráfico para HTML
    grafico_html = fig.to_html(full_html=False)
    
    return grafico_html