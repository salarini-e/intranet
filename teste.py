import csv
import pymysql
from pathlib import Path
from datetime import datetime


import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

BASE_DIR = Path(__file__).resolve().parent.parent

def load_envars(BASE_DIR):
    try:
        yaml_file=open("./.envvars.yaml", "r")        
    except:
        yaml_file=open(str(BASE_DIR.parent) + "/site/.envvars.yaml", "r")
        
    return yaml.load(yaml_file, Loader=Loader)

# Carregar variáveis de ambiente
env_vars = load_envars(BASE_DIR)


db_name = env_vars['db_name']
db_user = env_vars['db_user']
db_host = env_vars['db_host']
db_port = int(env_vars['db_port'])  # Conversão para int caso a porta esteja como string
db_passwd = env_vars['db_pw']

# Conectar ao banco de dados
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_passwd,
    database=db_name,
    port=db_port
)

cursor = connection.cursor()

# Caminho para o arquivo CSV
csv_file_path = str(BASE_DIR)+'/intranet/grdData.csv'


# Função para verificar se o funcionário deve ser incluído
def deve_incluir(situacao_funcional):
    situacao_funcional = situacao_funcional.lower()  # Converter para minúsculas para comparação
    return 'demitido' not in situacao_funcional and 'aposentado' not in situacao_funcional

# Abrir e ler o arquivo CSV
with open(csv_file_path, newline='', encoding='ANSI') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        situacao_funcional = row['Situação Funcional']
        
        # Verificar se a situação permite a inclusão do funcionário
        if not deve_incluir(situacao_funcional):
            continue

        nome = row['Nome']
        matricula = row['Matrícula']
        secretaria = row['Lotação']
        cpf = row['CPF']
        data_inclusao = datetime.now().strftime('%Y-%m-%d')  # Data atual formatada para o MySQL

        # Query para inserir o funcionário no banco de dados
        insert_query = """
            INSERT INTO instituicoes_meta_servidores (nome, matricula, secretaria, cpf, dt_inclusao)
            VALUES (%s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(insert_query, (nome, matricula, secretaria, cpf, data_inclusao))
            connection.commit()
            print(f"Funcionário {nome} inserido com sucesso.")
        except pymysql.MySQLError as e:
            print(f"Erro ao inserir {nome}: {e}")

# Fechar a conexão com o banco de dados
cursor.close()
connection.close()