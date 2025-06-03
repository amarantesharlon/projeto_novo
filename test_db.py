import requests
import psycopg2
import pandas as pd
import os
from dateutil.parser import parse

# 1. Consultar a API e obter o JSON
api_url = "https://dados.gov.br/dados/api/publico/conjuntos-dados/indice-desempenho-atendimento"
headers = {
    "accept": "application/json",
    "chave-api-dados-abertos": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJWZW02Z3JrTTFZVUVhSmE0SDRGU3hBaDJkdFRQMzVYc01TRWppSl9ZdV9heFYyZy1Bek9KSzNEQXZPc0dlbmRfU3otZHRHdmNFRzZiM3dqMyIsImlhdCI6MTc0ODc5MjYxN30.91xxuytt2bov67iXbTvKpAA8rPmmNKz6SS-nR6K5vfA"  # Substitua pelo seu token real
}
response = requests.get(api_url, headers=headers)
response.raise_for_status()
data = response.json()

# 2. Buscar todas as URLs com extensão .ods e filtrar por SCM, STFC e SMP
recursos = data.get('recursos', []) or data.get('result', {}).get('recursos', [])
ods_links = []
for r in recursos:
    formato = r.get('formato', '').lower()
    link = r.get('link', '')
    titulo = r.get('titulo', '').lower()
    if (
        formato == 'ods'
        and link
        and (
            'scm' in titulo
            or 'stfc' in titulo
            or 'smp' in titulo
        )
    ):
        ods_links.append((link.replace("\\", "/"), titulo))
print("Links ODS filtrados:", [l[0] for l in ods_links])

# Cria as pastas 'ods' e 'csvs' se não existirem
os.makedirs("ods", exist_ok=True)
os.makedirs("csvs", exist_ok=True)

# Conexão com o banco
conn = psycopg2.connect(
    host="db",
    database="meubanco",
    user="usuarioseguro",
    password="senhasegura",
)

def try_parse_date(val):
    try:
        return parse(val, dayfirst=True).strftime('%Y-%m-%d')
    except Exception:
        return val

for idx, (ods_url, titulo) in enumerate(ods_links):
    print(f"Baixando ODS: {ods_url}")
    nome_arquivo = os.path.basename(ods_url)
    ods_filename = f"ods/{nome_arquivo}"
    resp = requests.get(ods_url)
    with open(ods_filename, "wb") as f:
        f.write(resp.content)

    # Nome da tabela igual ao nome do arquivo ODS (sem extensão)
    table_name = os.path.splitext(nome_arquivo)[0]

    # Ler todas as abas do ODS, usando a linha 9 como header (header=8)
    df_dict = pd.read_excel(ods_filename, engine="odf", sheet_name=None, header=8)
    for t_idx, (sheet, df) in enumerate(df_dict.items()):
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        df.columns = [str(col).strip() for col in df.columns]
        df = df.drop_duplicates()
        df = df.fillna('')

        # Padroniza datas
        for col in df.columns:
            if df[col].astype(str).str.match(r'\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}').any():
                df[col] = df[col].astype(str).apply(try_parse_date)
        df = df.astype(str)

        # Salvar como CSV na pasta 'csvs'
        csv_filename = f"csvs/{table_name}.csv"
        df.to_csv(csv_filename, index=False, sep=';')
        print(f"Salvo CSV: {csv_filename}")

        # Criar tabela no Postgres e inserir os dados
        cur = conn.cursor()
        columns = ', '.join([f'"{str(col).strip()}" TEXT' for col in df.columns])
        cur.execute(f"""
        DROP TABLE IF EXISTS "{table_name}";
        CREATE TABLE "{table_name}" (
            {columns}
        );
        """)
        conn.commit()
        for _, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            col_names = ', '.join([f'"{str(col).strip()}"' for col in df.columns])
            cur.execute(
                f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})',
                tuple(row.astype(str))
            )
        conn.commit()
        cur.close()
        print(f"Dados da tabela {table_name} carregados com sucesso!")

conn.close()
print("Processo finalizado.")