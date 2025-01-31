import os
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurações
PASTA_MONITORADA = '/Users/gabrielmelo/Downloads'  # Pasta onde os arquivos são baixados
CREDENCIAIS_GOOGLE = 'credentials.json'  # Arquivo de credenciais do Google Sheets
NOME_PLANILHA = 'faturas nubank'  # Nome da planilha no Google Sheets
ABA_PLANILHA = 0  # Índice da aba (0 para a primeira aba)

# Configurações do Google Sheets
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIAIS_GOOGLE, SCOPE)
CLIENT = gspread.authorize(CREDS)

def processar_arquivo(caminho_arquivo):
    """Processa um arquivo CSV e faz o append dos dados na Google Sheet."""
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(caminho_arquivo)
        print(f"Arquivo processado: {caminho_arquivo}")

        # Converter dados para lista de listas
        dados = df.values.tolist()

        # Fazer o append na Google Sheet
        planilha = CLIENT.open(NOME_PLANILHA)
        aba = planilha.get_worksheet(ABA_PLANILHA)
        aba.append_rows(dados)
        print("Dados adicionados à planilha com sucesso!")

        # Mover o arquivo processado para uma pasta de backup (opcional)
        pasta_backup = os.path.join(PASTA_MONITORADA, 'processados')
        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup)
        os.rename(caminho_arquivo, os.path.join(pasta_backup, os.path.basename(caminho_arquivo)))

    except Exception as e:
        print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")

def monitorar_pasta():
    """Monitora a pasta em busca de novos arquivos CSV."""
    print(f"Monitorando a pasta: {PASTA_MONITORADA}")
    arquivos_processados = set()

    while True:
        # Listar arquivos na pasta
        arquivos = [f for f in os.listdir(PASTA_MONITORADA) if f.endswith('.csv') and os.path.isfile(os.path.join(PASTA_MONITORADA, f))]

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(PASTA_MONITORADA, arquivo)

            # Processar apenas novos arquivos
            if caminho_arquivo not in arquivos_processados:
                print(f"Novo arquivo detectado: {arquivo}")
                processar_arquivo(caminho_arquivo)
                arquivos_processados.add(caminho_arquivo)

        # Esperar antes de verificar novamente
        time.sleep(10)  # Verifica a cada 10 segundos

if __name__ == '__main__':
    monitorar_pasta()