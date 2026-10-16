import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_pokemon_batch(limit: int = 151) -> list:
    """
    Extrai dados em massa de múltiplos Pokémon da PokéAPI (ex: 1.ª Geração - 151 Pokémon).
    Percorre os IDs de 1 até ao limite definido.
    """
    pokemon_list = []
    base_url = "https://pokeapi.co/api/v2/pokemon"
    
    logging.info(f"A iniciar a extração em massa de {limit} Pokémon da PokéAPI...")
    
    for pokemon_id in range(1, limit + 1):
        url = f"{base_url}/{pokemon_id}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                pokemon_list.append(response.json())
            else:
                logging.warning(f"Aviso: Pokémon ID {pokemon_id} retornou status {response.status_code}")
        except Exception as e:
            logging.error(f"Erro ao extrair Pokémon ID {pokemon_id}: {e}")
            
    logging.info(f"✓ Extração concluída! Total de {len(pokemon_list)} Pokémon obtidos com sucesso.")
    return pokemon_list

if __name__ == "__main__":
    # Teste rápido executando o script diretamente
    data = extract_pokemon_batch(5)
    print(f"Testado com sucesso. Exemplo do primeiro Pokémon: {data[0]['name']}")