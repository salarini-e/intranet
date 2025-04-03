from django.shortcuts import render, HttpResponse
from ftplib import FTP
import pymysql

# Constants for FTP credentials
FTP_SERVER = '192.168.4.169'
FTP_USER = 'luiz_fabris'
FTP_PASSWORD = 'f1nh44'

# Constants for FTP paths
FTP_PATHS = {
    1: '/Volume_1/Parcelamentos/Imagens Escaneadas/Pasta ',
    4: '/Volume_1/Parcelamentos/Processos_Diversos/DIVERSAS/Pasta',
    7: '/Volume_1/Parcelamentos/Averbacoes-Fracao_Ideal/PROC_Pasta'
}

def imagem(request, primary_key):
    data = get_data_from_database(primary_key)
    if not data:
        return render(request, 'html_erro.html', {'msg': 'Dados não encontrados no banco de dados.'})

    if data['tipo'] in [2, 5, 6]:
        return HttpResponse("<script>alert('As Caixas/Pastas de Processos A Pagar e de Processos Indeferidos não podem ser acessadas!'); history.back();</script>")
    elif data['tipo'] == 3:
        return canudos_logic(data)

    pasta_ftp = FTP_PATHS.get(data['tipo'])
    if not pasta_ftp:
        return render(request, 'html_erro.html', {'msg': 'Tipo de pasta não suportado.'})

    proc = data['processo'].replace('/', '_')
    num_pasta, seq = data['pasta'].split('/')

    # Connect to FTP
    ftp = connect_to_ftp()
    if not ftp:
        return render(request, 'html_erro.html', {'msg': 'Falha na conexão com o Servidor FTP'})

    pasta_ftp = f"{pasta_ftp}{num_pasta.strip()}"
    try:
        lista_pastas = ftp.nlst(pasta_ftp)
    except Exception:
        return render(request, 'html_erro.html', {'msg': 'Erro ao listar diretórios no FTP'})

    if data['tipo'] == 4:
        proc = proc.split('_')[0]

    pesquisa = [
        {
            'servidor': FTP_SERVER,
            'pasta_ftp': pasta_ftp,
            'proc': p,
        }
        for p in lista_pastas
        if seq in p.split(' ')[0] and proc in p.split(' ')[3]
    ]

    if not pesquisa:
        return render(request, 'html_erro.html', {
            'msg': f'Processo não localizado. <br>Verifique na torradeira a pasta <br><br><a href="ftp:\\{FTP_SERVER}{pasta_ftp}">{pasta_ftp}/</a>'
        })

    for p in pesquisa:
        local_ftp = f"{pasta_ftp}/{p['proc']}"
        try:
            arquivos = ftp.nlst(local_ftp)
            p['arquivos'] = [arquivo for arquivo in arquivos if arquivo not in ['.', '..', 'Thumbs.db']]
        except Exception:
            return render(request, 'html_erro.html', {'msg': 'Erro ao listar arquivos no FTP'})

    ftp.quit()
    context = {'data': pesquisa}
    return render(request, 'ftp_view1.html', context)

def connect_to_ftp():
    try:
        ftp = FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.set_pasv(True)
        return ftp
    except Exception:
        return None

def get_data_from_database(primary_key):
    # Connect to the database
    connection = pymysql.connect(
        host='192.168.1.220',  # Updated database host
        user='mainterno',      # Updated database username
        password='f1nh44',     # Updated database password
        database='arquivo_dps' # Updated database name
    )
    try:
        with connection.cursor() as cursor:
            # Execute the query
            query = '''
                SELECT *
                FROM arquivo                 
                WHERE arquivo.id = %s
            '''
            cursor.execute(query, (primary_key,))
            result = cursor.fetchone()
            if result:
                # Map the result to a dictionary
                return {
                    'id': result[0],  # Adjust index based on your table structure
                    'nome': result[1],  # Adjust index based on your table structure
                    'processo': result[2],  # Adjust index based on your table structure
                    'informacao': result[3],  # Adjust index based on your table structure
                    'informacao_num': result[4],  # Adjust index based on your table structure
                    'endereco': result[5],  # Adjust index based on your table structure
                    'pasta': result[6],  # Adjust index based on your table structure'
                    'tipo_alfa': result[7],  # Adjust index based on your table structure
                    'tipo': result[8],  # Adjust index based on your table structure
                    'obs': result[9],  # Adjust index based on your table structure
                    'data_saida': result[10],  # Adjust index based on your table structure
                    'destino': result[11],  # Adjust index based on your table structure
                    'anexado': result[12],  # Adjust index based on your table structure
                    'saida_para': result[13],  # Adjust index based on your table structure                    
                }
            else:
                return None
    finally:
        connection.close()

def imagem_bkp(request, primary_key):
    # Replace PHP logic with Python/Django equivalents
    return HttpResponse("Imagem_bkp view logic here.")

def canudos(request, primary_key):
    # Replace PHP logic with Python/Django equivalents
    return HttpResponse("Canudos view logic here.")

def canudos_bkp(request, primary_key):
    # Replace PHP logic with Python/Django equivalents
    return HttpResponse("Canudos_bkp view logic here.")

def abre(request, arquivo):
    # Replace PHP logic with Python/Django equivalents
    return HttpResponse("Abre view logic here.")

def canudos_logic(data):
    # Placeholder for canudos logic
    return HttpResponse("Canudos logic here.")
