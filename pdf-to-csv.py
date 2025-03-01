
import openai
import pdfplumber
import pandas as pd
import re

# Configuração da chave da API do OpenAI (substitua pela sua chave)
openai.api_key = "sua-chave-api-aqui"

# Dicionário de categorias fixo
icone_para_categoria = {
    "carrinho de compras": "Supermercado",
    "garfo e faca": "Restaurante",
    "coração": "Saúde",
    "ônibus ou carro": "Transporte",
    "casa": "Casa",
    "livro ou lápis": "Educação",
    "cabo usb": "Eletrônicos",
    "ferramenta ou engrenagem": "Serviços",
    "bola, ingressos ou joystick": "Lazer"
}

# Função para interação com ChatGPT, delegando toda a categorização a ele
def categorizar_transacao_com_chatgpt(titulo):
    categorias_disponiveis = ", ".join(icone_para_categoria.values())
    prompt = (f"Dado o título de uma transação de fatura do cartão: '{titulo}', "
              f"categorize a transação de acordo com as seguintes categorias: "
              f"{categorias_disponiveis}. "
              f"Responda apenas com a categoria mais apropriada, sem explicações adicionais.")
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=50,
        temperature=0.3,
    )
    
    return response.choices[0].text.strip()

# Função principal para extrair transações e categorizá-las com ChatGPT
def extrair_e_categorizar_transacoes(pdf_path, output_csv_base):
    transacoes = []
    mes_fatura = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                linhas = text.split("\n")
                for linha in linhas:
                    if re.search(r"FATURA.*\b([A-Z]{3})\b", linha):
                        mes_fatura = re.search(r"FATURA.*\b([A-Z]{3})\b", linha).group(1)
                    match = re.search(r"(\d{2} [A-Z]{3}) (.+?) (R\$ [-\d.,]+)", linha)
                    if match:
                        data, titulo, valor = match.groups()
                        valor = float(valor.replace("R$", "").replace(",", "."))
                        
                        # Categorização via ChatGPT
                        categoria = categorizar_transacao_com_chatgpt(titulo)
                        transacoes.append([data, categoria, titulo, valor])

    df = pd.DataFrame(transacoes, columns=["Data", "Categoria", "Título", "Valor"])
    
    if mes_fatura:
        output_csv = f"{output_csv_base.replace('.csv', '')}_{mes_fatura}.csv"
    else:
        output_csv = output_csv_base
    
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Arquivo CSV salvo em: {output_csv}")

# Exemplo de uso:
# extrair_e_categorizar_transacoes("caminho/para/fatura.pdf", "transacoes_nubank.csv")
