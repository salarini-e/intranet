import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


import openpyxl
excel_file_path = "dados.xlsx"


options = webdriver.ChromeOptions()    

# Inicialização do driver do Chrome
driver = webdriver.Chrome(options=options)

url = "https://novafriburgo-rj.portaltp.com.br/consultas/pessoal/servidores.aspx"
driver.get(url)

# Aguarda até que a tabela de dados seja carregada
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

data = []

while True:
    # Encontre a tabela no HTML
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if len(cols) >= 3:
            col_2 = cols[1].text.strip()
            col_3 = cols[2].text.strip()
            data.append([col_2, col_3])

    try:

        # Encontre o botão "Próximo" e clique nele
        next_button = driver.find_element(By.XPATH, '//a[@data-args="PBN"]')
        next_button.click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-args="PBN"]')))
        time.sleep(4)  # Aguarde um pouco para que a próxima página seja carregada
    except:
        # Se não houver mais botão "Próximo", saia do loop
        break

# Fechar o navegador após a coleta de dados
driver.quit()

# Criar um DataFrame pandas com os dados coletados
df = pd.DataFrame(data, columns=["Coluna 2", "Coluna 3"])

df.to_excel(excel_file_path, index=False)

workbook = openpyxl.load_workbook(excel_file_path)
worksheet = workbook.active

# Definir largura automática das colunas
for column_cells in worksheet.columns:
    length = max(len(str(cell.value)) for cell in column_cells)
    worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

# Salvar as alterações no arquivo Excel
workbook.save(excel_file_path)