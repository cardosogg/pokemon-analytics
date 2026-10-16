import os
import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_USER = "airflow"
DB_PASSWORD = "airflow"
DB_HOST = "postgres"  # Nome do serviço no Docker Compose
DB_PORT = "5432"
DB_NAME = "airflow"

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_to_postgres(table_name: str, df: pd.DataFrame):
    """
    Recebe o DataFrame limpo e carrega-o em lote (bulk insert) 
    para uma tabela no PostgreSQL.
    """
    logging.info("A estabelecer ligação ao PostgreSQL...")
    engine = create_engine(DATABASE_URL)
    
    logging.info(f"A carregar {len(df)} registos para a tabela '{table_name}'...")
    
    # 'replace' substitui a tabela inteira a cada execução
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    
    logging.info(f"✓ Dados carregados com sucesso para a tabela '{table_name}'!")