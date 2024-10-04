import csv
import pymysql
from pathlib import Path
from datetime import datetime
import yaml
import os


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do arquivo de log
log_file_path = str(BASE_DIR) + "\intranet\data_log.txt"

def log(message):
    """Escreve mensagens no arquivo de log com a data e hora atual."""
    log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"
    
    # Verifica se o arquivo já existe
    if os.path.exists(log_file_path):
        mode = 'a'  # Abre o arquivo para anexar mensagens
    else:
        mode = 'w'  # Cria um novo arquivo se não existir

    with open(log_file_path, mode) as log_file:
        log_file.write(log_message)
    
    print(log_message)  # Também imprime no console

def load_envars(base_dir):
    """Carrega as variáveis de ambiente a partir de um arquivo YAML."""
    try:
        yaml_file = open("./.envvars.yaml", "r")
    except FileNotFoundError:
        yaml_file = open(str(base_dir.parent) + "/site/.envvars.yaml", "r")
        
    return yaml.load(yaml_file, Loader=Loader)

def connect_db(env_vars):
    """Conecta ao banco de dados usando as variáveis de ambiente carregadas."""
    return pymysql.connect(
        host=env_vars['db_host'],
        user=env_vars['db_user'],
        password=env_vars['db_pw'],
        database=env_vars['db_name'],
        port=int(env_vars['db_port'])  # Conversão para int caso a porta esteja como string
    )

def deve_incluir(situacao_funcional):
    """Verifica se o funcionário deve ser incluído com base na situação funcional."""
    situacao_funcional = situacao_funcional.lower()  # Converter para minúsculas para comparação
    return 'demitido' not in situacao_funcional and 'aposentado' not in situacao_funcional

def processar_csv(csv_file_path, cursor):
    """Processa o arquivo CSV e insere os dados no banco de dados."""
    
    # Apagar todos os registros da tabela antes de inserir novos dados
    delete_query = "DELETE FROM instituicoes_meta_servidores"
    try:
        cursor.execute(delete_query)
        log("Todos os registros anteriores foram apagados com sucesso.")
    except pymysql.MySQLError as e:
        log(f"Erro ao apagar registros anteriores: {e}")

    # Processar o CSV e inserir novos registros
    # with open(csv_file_path, newline='', encoding='ANSI') as csvfile:
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            situacao_funcional = row['Situação Funcional']
            
            if not deve_incluir(situacao_funcional):
                continue

            nome = row['Nome']
            matricula = row['Matrícula']
            secretaria = row['Lotação']
            cpf = row['CPF']
            data_inclusao = datetime.now().strftime('%Y-%m-%d')  # Data atual formatada para o MySQL

            insert_query = """
                INSERT INTO instituicoes_meta_servidores (nome, matricula, secretaria, cpf, dt_inclusao)
                VALUES (%s, %s, %s, %s, %s)
            """

            try:
                cursor.execute(insert_query, (nome, matricula, secretaria, cpf, data_inclusao))
            except pymysql.MySQLError as e:
                log(f"Erro ao inserir {nome}: {e}")

def main():
    """Função principal que orquestra a execução do script."""
    # Carregar variáveis de ambiente
    env_vars = load_envars(BASE_DIR)

    # Conectar ao banco de dados
    connection = connect_db(env_vars)
    cursor = connection.cursor()

    # Caminho para o arquivo CSV
    csv_file_path = str(BASE_DIR) + '/intranet/grdData.csv'

    # Processar o arquivo CSV
    processar_csv(csv_file_path, cursor)

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
