from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys

sys.path.insert(0, '/opt/airflow/src')

from transform_data import transform_pokemon_data
from load_data import load_to_postgres

@dag(
    dag_id='pokemon_portfolio_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL Portefólio - PokéAPI (1.ª Geração) & PostgreSQL',
    schedule='0 */1 * * *',
    start_date=datetime(2026, 2, 7),
    catchup=False,
    tags=['pokemon', 'etl', 'portfolio', 'engineering']
)
def pokemon_pipeline():
    
    @task
    def extract_and_transform():
        """Executa a extração em massa dos 151 Pokémon e aplica as transformações."""
        df = transform_pokemon_data(limit=151)
        # Guarda temporariamente em Parquet para passar entre as tasks do Airflow
        df.to_parquet('/opt/airflow/data/temp_pokemon_batch.parquet', index=False)
        
    @task 
    def load():
        """Lê os dados processados e envia-os para a tabela do PostgreSQL."""
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_pokemon_batch.parquet')
        load_to_postgres('pokemon_stats', df)
        
    extract_and_transform() >> load()

pokemon_pipeline()