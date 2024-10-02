import csv
import os
from django.conf import settings
from instituicoes.models import Meta_Servidores

from django.core.management.base import BaseCommand

def processar_csv():
    # Caminho completo do arquivo CSV
    csv_path = os.path.join(settings.BASE_DIR, 'grdData.csv')
    
    # Definindo o caminho para o arquivo de log
    log_path = os.path.join(settings.BASE_DIR, 'matriculas_nao_encontradas.csv')
    
    # Abrindo o arquivo CSV para leitura
    with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        # Lista para armazenar matrículas não encontradas
        matriculas_nao_encontradas = []
        matriculas_nao_encontradas.append(f';Matricula;Nome;Secretaria;CPF')
        # Iterar sobre cada linha do CSV
        for row in reader:
            matricula = row['Matricula']  # Corrija a codificação do arquivo para evitar problemas com acentuação
            nome = row['Nome']
            secretaria = row['Lotacao']
            cpf = row['CPF']

            try:
                # Verificar se a matrícula já existe no banco de dados
                servidor = Meta_Servidores.objects.get(matricula=matricula)
                # print(f'Matrícula {matricula} - {nome} encontrada no banco de dados.')
            except Meta_Servidores.DoesNotExist:
                # Caso a matrícula não seja encontrada, adiciona à lista de não encontradas
                # print(f'Matrícula {matricula} - {nome} não encontrada no banco de dados.')
                matriculas_nao_encontradas.append(f';{matricula};{nome};{secretaria};{cpf}')
        
        # Escrever as matrículas não encontradas no arquivo de log
        with open(log_path, 'w') as log_file:
            for matricula in matriculas_nao_encontradas:
                log_file.write(f'{matricula}\n')

    print(f'Processamento finalizado. Verifique o arquivo de log: {log_path}')

class Command(BaseCommand):
    help = 'Processa o arquivo grdData.csv e verifica as matrículas no banco de dados'

    def handle(self, *args, **kwargs):
        processar_csv()
        self.stdout.write(self.style.SUCCESS('Processamento finalizado com sucesso!'))
