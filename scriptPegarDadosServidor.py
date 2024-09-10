from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import yaml
from pathlib import Path
import os
import time
import sys

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

chrome_options = Options()
chrome_options.add_argument("--headless")

BASE_DIR = Path(__file__).resolve().parent.parent

def load_envars(BASE_DIR):
    try:
        yaml_file = open("./.envvars.yaml", "r")        
    except:
        yaml_file = open(str(BASE_DIR.parent) + "/site/.envvars.yaml", "r")
        
    return yaml.load(yaml_file, Loader=Loader)

# Carregar variáveis de ambiente
env_vars = load_envars(BASE_DIR)

# Configurações de download
download_dir = str(BASE_DIR) + "\intranet"
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://novafriburgo-rj.portaltp.com.br/consultas/pessoal/servidores.aspx")

    # Elemento que contem a data de atualizacao dos servidores
    elemento_samp = driver.find_element(By.CLASS_NAME, 'info-data-atualizacao-outline')
    lancado = elemento_samp.text
    date = lancado.split()[-1] #pega apenas a data, sem o texto
    # print("Texto site:", lancado)
    # print("Data Completa:", date)

    data_hoje = datetime.today()
    data_hoje_formatada = data_hoje.strftime("%d/%m/%Y")
    print("Data de hoje formatada:", data_hoje_formatada)

    #caso a data de atualizacao seja a data do dia atual, deve baixar o novo arquivo .csv dos servidores, para manter sempre atualizado
    if data_hoje_formatada == date:
        print("Datas iguais - Clicando no botão 'Imprimir Relatório'")
        
        #pega o botão "Imprimir Relatório"
        botao_imprimir = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ctl00_containerCorpo_grdData_DXCTMenu0_DXI2_T'))
        )
        botao_imprimir.click()

        #Pega o botão "csv" após ter clicado no botão para Imprimir o Relatório
        link_desejado = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_containerCorpo_grdData_DXCTMenu0_DXI2i4_T'))
        )
        link_desejado.click()

        # Aguarda o download ser concluído
        tempo_espera = 0
        arquivo_baixado = False
        nome_arquivo = "grdData.csv"  # Nome esperado do arquivo quando baixado pelo site

        # Verifica se o arquivo já existe e remove-o, se necessário
        arquivo_path = os.path.join(download_dir, nome_arquivo)
        if os.path.exists(arquivo_path):
            print("Arquivo existente encontrado. Removendo...")
            os.remove(arquivo_path)

        # Espera até que o arquivo seja baixado
        while tempo_espera < 60:  # Aguarda até 60 segundos
            arquivos = os.listdir(download_dir)
            if nome_arquivo in arquivos:
                print("Arquivo baixado:", nome_arquivo)
                arquivo_baixado = True
                break
            time.sleep(5)  # Espera 5 segundos antes de verificar novamente
            tempo_espera += 5

        if not arquivo_baixado:
            print("Tempo esgotado - Arquivo não encontrado.")
    #se n for, n precisa fazer nada
    else:
        print("Datas diferentes")
        
finally:
    driver.quit()
