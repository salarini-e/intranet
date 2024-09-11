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
from data_import import main, log

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

BASE_DIR = Path(__file__).resolve().parent.parent


def load_envars(base_dir):
    """Carrega as variáveis de ambiente a partir de um arquivo YAML."""
    try:
        yaml_file = open("./.envvars.yaml", "r")        
    except FileNotFoundError:
        yaml_file = open(str(base_dir.parent) + "/site/.envvars.yaml", "r")
        
    return yaml.load(yaml_file, Loader=Loader)

def configurar_chrome(download_dir):
    """Configura o navegador Chrome com as opções desejadas."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    return chrome_options

def verificar_data_atualizacao(driver):
    """Verifica a data de atualização no site e retorna se deve fazer o download."""
    driver.get("https://novafriburgo-rj.portaltp.com.br/consultas/pessoal/servidores.aspx")
    elemento_samp = driver.find_element(By.CLASS_NAME, 'info-data-atualizacao-outline')
    lancado = elemento_samp.text
    date = lancado.split()[-1]  # Pega apenas a data, sem o texto

    data_hoje_formatada = datetime.today().strftime("%d/%m/%Y")

    if data_hoje_formatada == date:
        log("Datas iguais - prosseguindo com o download")
        return True
    else:
        log("Nenhuma ação necessária - Datas diferentes")

        return False

def baixar_arquivo_csv(driver, download_dir):
    """Baixa o arquivo CSV de servidores do site."""
    
    # Clicar no botão "Imprimir Relatório"
    botao_imprimir = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'ctl00_containerCorpo_grdData_DXCTMenu0_DXI2_T'))
    )
    botao_imprimir.click()

    # Clicar no botão "CSV"
    link_desejado = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'ctl00_containerCorpo_grdData_DXCTMenu0_DXI2i4_T'))
    )
    link_desejado.click()

    # Aguarda o download ser concluído
    nome_arquivo = "grdData.csv"
    arquivo_path = os.path.join(download_dir, nome_arquivo)

    if os.path.exists(arquivo_path):
        log("Arquivo existente encontrado. Removendo...")
        os.remove(arquivo_path)
        time.sleep(15)
    
    tempo_espera = 0
    while tempo_espera < 60:
        if nome_arquivo in os.listdir(download_dir):
            log(f"Arquivo baixado com sucesso: {nome_arquivo}")
            return True
        time.sleep(5)
        tempo_espera += 5

    log("Tempo esgotado - Arquivo nao encontrado.")
    return False

def main_script():
    """Função principal para execução do script."""
    # Carregar variáveis de ambiente
    env_vars = load_envars(BASE_DIR)

    # Configurar o Chrome
    download_dir = str(BASE_DIR) + "\intranet"
    chrome_options = configurar_chrome(download_dir)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        if verificar_data_atualizacao(driver):
            if baixar_arquivo_csv(driver, download_dir):
                main()  # Chama o script de importação de dados se o download for concluído
    finally:
        driver.quit()

if __name__ == "__main__":
    main_script()
