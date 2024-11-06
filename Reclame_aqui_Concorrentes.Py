from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import pandas as pd
import schedule

def coletar_dados_reclameaqui(url, nome_empresa):
    servico = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    navegador = webdriver.Chrome(service=servico, options=options)
    navegador.get(url)
    time.sleep(2)

    try:
        navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/a[1]').click()
    except NoSuchElementException:
        print("Botão de cookies não encontrado ou já aceito")

    navegador.execute_script("window.scrollBy(0, 500)")

    periodos = {
        'seis_meses': '//*[@id="newPerformanceCard-tab-1"]',
        'doze_meses': '//*[@id="newPerformanceCard-tab-2"]',
        'geral': '//*[@id="newPerformanceCard-tab-5"]'
    }

    elementos = {
        'nota_geral': '//*[@id="ra-new-reputation"]/span/b',
        'num_reclamacoes': '//*[@id="newPerformanceCard"]/div[2]/div[1]/span/strong',
        'Per_respondidas': '//*[@id="newPerformanceCard"]/div[2]/div[2]/span/strong',
        'novam_negoc': '//*[@id="newPerformanceCard"]/div[2]/div[5]/span/strong',
        'indice_solucao': '//*[@id="newPerformanceCard"]/div[2]/div[6]/span/strong',
        'Tempo_de_resposta': '//*[@id="newPerformanceCard"]/div[2]/div[7]/span/strong'
    }

    listas = {
        'nota_geral': [],
        'num_reclamacoes': [],
        'Per_respondidas': [],
        'novam_negoc': [],
        'indice_solucao': [],
        'Tempo_de_resposta': []
    }

    agora = datetime.datetime.now()

    for periodo in periodos:
        time.sleep(1)

        try:
            navegador.find_element(By.XPATH, periodos[periodo]).click()
        except NoSuchElementException:
            print(f"Período {periodo} não encontrado na página {url}")
            continue

        time.sleep(1)

        for elemento in elementos:
            try:
                element = navegador.find_element(By.XPATH, elementos[elemento])
                text = element.text
            except NoSuchElementException:
                print(f"Elemento {elemento} não encontrado na página {url}")
                text = "N/A"

            listas[elemento].append(text)

    navegador.quit()

    df_resumo = pd.DataFrame(listas)
    df_resumo['data'] = agora.date()
    df_resumo['hora'] = agora.time()
    df_resumo['periodo'] = ['Últimos 6 meses', 'Últimos 12 meses', 'Geral']

    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    nome_arquivo = f"Reclame_aqui_{nome_empresa}_{data_atual}.xlsx"
    caminho_saida = fr'C:\Users\Diogo Souza\Desktop\{nome_arquivo}'
    df_resumo.to_excel(caminho_saida, index=False)

def job():
    # Lista de URLs e nomes de empresas
    urls = {
        'Amazon': 'https://www.reclameaqui.com.br/empresa/amazon/',
        'Mercado-Livre': 'https://www.reclameaqui.com.br/empresa/mercado-livre/',
        'Shopee': 'https://www.reclameaqui.com.br/empresa/shopee/'
    }

    # Executar a coleta de dados para cada URL
    for nome_empresa, url in urls.items():
        coletar_dados_reclameaqui(url, nome_empresa)

    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    print("Tarefa realizada com sucesso às", hora_atual)

# Agendar a tarefa para ser executada todos os dias às 17h
schedule.every().day.at("14:23").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
