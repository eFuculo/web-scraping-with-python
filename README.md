#**Coletor de Dados Reclame Aqui**

Este projeto automatiza a coleta de dados de reputação de empresas no site Reclame Aqui. Com o uso da biblioteca Selenium, o script acessa as páginas das empresas, extrai informações relevantes e armazena os dados em um arquivo Excel. A coleta de dados é configurada para ser executada automaticamente diariamente, em um horário especificado.

- Pré-requisitos:
Para executar este script, é necessário instalar as seguintes bibliotecas:

Selenium para automação do navegador:
bash
Copiar código
pip install selenium
webdriver-manager para facilitar o gerenciamento do driver do Chrome:
bash
Copiar código
pip install webdriver-manager
Pandas para manipulação e exportação de dados:
bash
Copiar código
pip install pandas
Schedule para agendamento da execução do script:
bash
Copiar código
pip install schedule
Estrutura do Código
1. Importação de Bibliotecas
python
Copiar código
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import pandas as pd
import schedule
Essas bibliotecas permitem controle do navegador, manipulação de dados e agendamento de tarefas.

2. Função coletar_dados_reclameaqui
Esta função acessa o site Reclame Aqui, coleta informações sobre a reputação das empresas e exporta esses dados para um arquivo Excel.

Parâmetros:

url: URL da página Reclame Aqui da empresa.
nome_empresa: Nome da empresa para identificar o arquivo de saída.
Passo a Passo:

Configuração e Abertura do Navegador:

python
Copiar código
servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
navegador = webdriver.Chrome(service=servico, options=options)
navegador.get(url)
time.sleep(2)
Configura o driver do Chrome e abre a página especificada.

Aceitar Cookies:

python
Copiar código
try:
    navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/a[1]').click()
except NoSuchElementException:
    print("Botão de cookies não encontrado ou já aceito")
Clica no botão de aceitação de cookies, se necessário.

Definir Seletores e Estruturas de Dados:

python
Copiar código
periodos = {...}
elementos = {...}
listas = {...}
Define XPaths para selecionar períodos e elementos de dados e cria dicionários para armazenar as informações coletadas.

Coletar Dados para Diferentes Períodos:

python
Copiar código
for periodo in periodos:
    time.sleep(1)
    try:
        navegador.find_element(By.XPATH, periodos[periodo]).click()
    ...
Para cada período, o script clica no botão correspondente e coleta dados como nota_geral, num_reclamacoes, Per_respondidas, entre outros.

Exportação dos Dados para Excel:

python
Copiar código
df_resumo = pd.DataFrame(listas)
df_resumo['data'] = agora.date()
df_resumo['hora'] = agora.time()
df_resumo['periodo'] = ['Últimos 6 meses', 'Últimos 12 meses', 'Geral']
Armazena os dados coletados em um DataFrame e os exporta para um arquivo Excel no formato Reclame_aqui_<nome_empresa>_<data_atual>.xlsx.

3. Função job
A função job organiza a execução de coletar_dados_reclameaqui para uma lista de URLs de empresas.

python
Copiar código
def job():
    urls = {
        'Amazon': 'https://www.reclameaqui.com.br/empresa/amazon/',
        'Mercado-Livre': 'https://www.reclameaqui.com.br/empresa/mercado-livre/',
        'Shopee': 'https://www.reclameaqui.com.br/empresa/shopee/'
    }

    for nome_empresa, url in urls.items():
        coletar_dados_reclameaqui(url, nome_empresa)

    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    print("Tarefa realizada com sucesso às", hora_atual)
Essa função executa coletar_dados_reclameaqui para cada URL da empresa e imprime uma mensagem indicando a hora em que a tarefa foi realizada com sucesso.

4. Agendamento com schedule
python
Copiar código
schedule.every().day.at("14:23").do(job)
Esta linha agenda a execução da função job todos os dias às 14:23. Você pode alterar o horário conforme necessário.

5. Loop de Execução
python
Copiar código
while True:
    schedule.run_pending()
    time.sleep(1)
Esse loop mantém o script em execução, verificando periodicamente se há alguma tarefa agendada para ser executada.

Personalização
Para adaptar este código, você pode:

Alterar as URLs no dicionário urls para incluir as páginas Reclame Aqui de outras empresas.
Alterar o horário de execução no comando schedule.every().day.at("14:23").do(job).
Observações
Certifique-se de que o navegador Chrome está instalado, pois o webdriver_manager instalará a versão mais recente do ChromeDriver automaticamente.
O código é configurado para Windows, com o caminho de saída do arquivo Excel no desktop (C:\Users\Diogo Souza\Desktop). Atualize o caminho conforme necessário para seu sistema operacional.
Exemplo de Execução
Ao executar o script, o navegador abrirá, navegará para cada URL especificada, coletará os dados e fechará o navegador. O arquivo Excel com os dados coletados será salvo na área de trabalho.
