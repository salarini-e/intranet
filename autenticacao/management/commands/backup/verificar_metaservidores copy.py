import csv
import os
from django.conf import settings
from instituicoes.models import Meta_Servidores

from django.core.management.base import BaseCommand

# processa arquivo do portal de transparência e gera novo arquivo
def processar_csv():
    # Caminho completo do arquivo CSV
    csv_path = os.path.join(settings.MEDIA_ROOT, 'grdData.csv')

    # Substituir a primeira linha do arquivo CSV pelo novo cabeçalho
    novo_cabecalho = 'Detalhes;Matricula;Nome;Lotacao;CPF;Vinculo;Cargo;Admissao;Demissao;Ano;Mes;Situacao Funcional\n'

    with open(csv_path, 'r', encoding='ISO-8859-1') as f:
        linhas = f.readlines()

    if linhas:
        linhas[0] = novo_cabecalho
        with open(csv_path, 'w', encoding='ISO-8859-1') as f:
            f.writelines(linhas)    

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
                # servidor.delete()

                matriculas_nao_encontradas.append(f';{matricula};{nome};{secretaria};{cpf}')    
            
            except Meta_Servidores.DoesNotExist:
                # Caso a matrícula não seja encontrada, adiciona à lista de não encontradas 
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
