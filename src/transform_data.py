import pandas as pd
from extract_data import extract_pokemon_batch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_pokemon_data(limit: int = 151) -> pd.DataFrame:
    """
    Recebe a lista de JSONs brutos da PokéAPI, limpa, estrutura
    e transforma num DataFrame limpo do Pandas pronto para análise.
    """
    raw_data_list = extract_pokemon_batch(limit)
    parsed_data = []
    
    logging.info("A iniciar a transformação dos dados dos Pokémon...")
    
    for pokemon in raw_data_list:
        # 1. Extração segura de estatísticas (stats) que vêm numa lista aninhada no JSON
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon.get('stats', [])}
        
        # 2. Extração segura do tipo principal
        types = pokemon.get('types', [])
        primary_type = types[0]['type']['name'] if types else None
        
        # 3. Montar o dicionário estruturado para este Pokémon específico
        parsed_pokemon = {
            "pokedex_id": pokemon.get("id"),
            "pokemon_name": pokemon.get("name"),
            "height_m": pokemon.get("height", 0) / 10.0,      # Convertido de decímetros para metros
            "weight_kg": pokemon.get("weight", 0) / 10.0,    # Convertido de hectogramas para quilogramas
            "base_experience": pokemon.get("base_experience", 0),
            "primary_type": primary_type,
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
            "special_attack": stats.get("special-attack", 0),
            "special_defense": stats.get("special-defense", 0),
            "speed": stats.get("speed", 0)
        }
        parsed_data.append(parsed_pokemon)
        
    # Converter a lista de dicionários num DataFrame consolidado do Pandas
    df = pd.DataFrame(parsed_data)
    
    # 4. Engenharia de Atributos (Criação de uma métrica analítica nova)
    # Evita divisão por zero caso a altura seja nula
    df['bmi_approx'] = round(df['weight_kg'] / (df['height_m'] ** 2), 2)
    
    logging.info(f"✓ Transformação concluída! DataFrame gerado com {len(df)} linhas e {len(df.columns)} colunas.")
    return df

if __name__ == "__main__":
    # Teste rápido executando o script isoladamente
    df_test = transform_pokemon_data(5)
    print("\n--- Exemplo do DataFrame Transformado ---")
    print(df_test[['pokedex_id', 'pokemon_name', 'primary_type', 'attack', 'speed']].head())