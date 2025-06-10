import csv
import os
from django.conf import settings
from instituicoes.models import Meta_Servidores

from django.core.management.base import BaseCommand


# cadastra de acordo com o arquivo gerado
def cadastrar_nao_encontrados():
    # Caminho completo do arquivo CSV
    csv_path = os.path.join(settings.BASE_DIR, 'matriculas_nao_encontradas.csv')    
    # Definindo o caminho para o arquivo de log
    log_path = os.path.join(settings.BASE_DIR, 'error_cadastrar_nao_encontradas.log')
    
    # Abrindo o arquivo CSV para leitura
    with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        # Lista para armazenar matrículas não encontradas
        logs = []

        # Iterar sobre cada linha do CSV
        for row in reader:
            matricula = row['Matricula']  # Corrija a codificação do arquivo para evitar problemas com acentuação
            nome = row['Nome']
            secretaria = row['Secretaria']
            cpf = row['CPF']

            try:
                Meta_Servidores.objects.create(                    
                    nome=nome,
                    matricula=matricula,                    
                    secretaria=secretaria,
                    cpf=cpf
                )
            except Exception as e:
                # Caso a matrícula não seja encontrada, adiciona à lista de não encontradas
                # print(f'Matrícula {matricula} - {nome} não encontrada no banco de dados.')
                logs.append(f'erros: {matricula} - {e}')
        
        # Escrever as matrículas não encontradas no arquivo de log
        with open(log_path, 'w') as log_file:
            for log in logs:
                log_file.write(f'{log}\n')

    print(f'Processamento finalizado. Verifique o arquivo de log: {log_path}')

class Command(BaseCommand):
    help = 'Processa o arquivo matriculas_nao_encontradas.csv e cadastras as matrículas no banco de dados'

    def handle(self, *args, **kwargs):
        cadastrar_nao_encontrados()
        self.stdout.write(self.style.SUCCESS('Processamento finalizado!'))
