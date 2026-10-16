import os
import logging
import traceback
from dotenv import load_dotenv

load_dotenv('config/.env')

from src.extract_data import extract_weather_data
from src.transform_data import data_transformations
from src.load_data import load_to_postgres

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pipeline():
    try:
        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError("API_KEY não encontrada! Verifique o ficheiro config/.env")
            
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={api_key}"

        logging.info("ETAPA 1: EXTRACT")
        extract_weather_data(url)

        logging.info("ETAPA 2: TRANSFORM")
        df = data_transformations()

        logging.info("ETAPA 3: LOAD")
        # Passa o df gerado diretamente para a carga
        load_to_postgres(df)

        print("\n" + "="*60)
        print("✓ Pipeline concluído com sucesso!")
        print("="*60)

    except Exception as e:
        logging.error(f"❌ ERRO no Pipeline: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    pipeline()