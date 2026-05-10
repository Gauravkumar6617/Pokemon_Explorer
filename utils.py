import requests
import time
from functools import lru_cache

BASE_URL = "https://pokeapi.co/api/v2/"

# Cache for API calls to reduce requests
@lru_cache(maxsize=500)
def get_pokemon_data(pokemon_name_or_id):
    """Fetches data for a given Pokémon by name or ID."""
    url = f"{BASE_URL}pokemon/{pokemon_name_or_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Pokémon data: {e}")
        return None

@lru_cache(maxsize=500)
def get_pokemon_species_data(pokemon_name_or_id):
    """Fetches species data including evolution chain for a Pokémon."""
    try:
        species_url = f"{BASE_URL}pokemon-species/{pokemon_name_or_id}"
        species_response = requests.get(species_url, timeout=10)
        species_response.raise_for_status()
        species_data = species_response.json()
        
        # Get evolution chain
        evo_chain_url = species_data.get("evolution_chain", {}).get("url")
        evolution_chain = []
        
        if evo_chain_url:
            try:
                evo_chain_response = requests.get(evo_chain_url, timeout=10)
                evo_chain_response.raise_for_status()
                
                def traverse(node):
                    evolution_chain.append(node["species"]["name"])
                    for evo in node.get("evolves_to", []):
                        traverse(evo)
                
                traverse(evo_chain_response.json()["chain"])
            except:
                pass
        
        # Add evolution chain to species data
        species_data['evolution_chain'] = evolution_chain
        return species_data
        
    except requests.RequestException as e:
        print(f"Error fetching evolution chain: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected JSON structure: {e}")
        return None

@lru_cache(maxsize=200)
def get_ability_data(ability_name):
    """Fetches detailed ability data."""
    url = f"{BASE_URL}ability/{ability_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching ability data: {e}")
        return None

@lru_cache(maxsize=500)
def get_move_data(move_name):
    """Fetches detailed move data."""
    url = f"{BASE_URL}move/{move_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching move data: {e}")
        return None

def compare_pokemon_stats(pokemon_list):
    """
    Compare stats of multiple Pokémon.
    
    Args:
        pokemon_list: List of Pokémon names or IDs
    
    Returns:
        Dictionary with comparison data
    """
    comparison = {
        'pokemon': [],
        'stats': {}
    }
    
    stat_names = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    
    for stat in stat_names:
        comparison['stats'][stat] = []
    
    for pokemon in pokemon_list:
        data = get_pokemon_data(pokemon)
        if data:
            comparison['pokemon'].append(data['name'])
            for stat in data['stats']:
                stat_name = stat['stat']['name']
                if stat_name in comparison['stats']:
                    comparison['stats'][stat_name].append(stat['base_stat'])
    
    return comparison

@lru_cache(maxsize=50)
def get_type_effectiveness(type_name):
    """
    Get type effectiveness data (strengths and weaknesses).
    
    Args:
        type_name: Name of the type
    
    Returns:
        Dictionary with effectiveness data
    """
    url = f"{BASE_URL}type/{type_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        effectiveness = {
            'double_damage_from': [t['name'] for t in data['damage_relations']['double_damage_from']],
            'half_damage_from': [t['name'] for t in data['damage_relations']['half_damage_from']],
            'no_damage_from': [t['name'] for t in data['damage_relations']['no_damage_from']],
            'double_damage_to': [t['name'] for t in data['damage_relations']['double_damage_to']],
            'half_damage_to': [t['name'] for t in data['damage_relations']['half_damage_to']],
            'no_damage_to': [t['name'] for t in data['damage_relations']['no_damage_to']]
        }
        
        return effectiveness
    except requests.RequestException as e:
        print(f"Error fetching type effectiveness: {e}")
        return None

@lru_cache(maxsize=50)
def search_pokemon_by_type(type_name):
    """
    Search for Pokémon by type.
    
    Args:
        type_name: Name of the type to search for
    
    Returns:
        List of Pokémon names with that type
    """
    url = f"{BASE_URL}type/{type_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        pokemon_list = [p['pokemon']['name'] for p in data['pokemon']]
        return pokemon_list
    except requests.RequestException as e:
        print(f"Error searching by type: {e}")
        return []

def get_pokemon_encounters(pokemon_id):
    """
    Get encounter locations for a Pokémon.
    
    Args:
        pokemon_id: ID of the Pokémon
    
    Returns:
        List of location areas
    """
    url = f"{BASE_URL}pokemon/{pokemon_id}/encounters"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        locations = []
        for encounter in data:
            location_area = encounter['location_area']['name']
            locations.append(location_area.replace('-', ' ').title())
        
        return locations
    except requests.RequestException as e:
        print(f"Error fetching encounters: {e}")
        return []

@lru_cache(maxsize=100)
def get_generation_data(generation_id):
    """
    Get data for a specific generation.
    
    Args:
        generation_id: ID or name of the generation
    
    Returns:
        Generation data including Pokémon list
    """
    url = f"{BASE_URL}generation/{generation_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        generation_info = {
            'name': data['name'],
            'pokemon_species': [p['name'] for p in data['pokemon_species']],
            'main_region': data['main_region']['name'],
            'types': [t['name'] for t in data.get('types', [])]
        }
        
        return generation_info
    except requests.RequestException as e:
        print(f"Error fetching generation data: {e}")
        return None

def get_pokemon_by_habitat(habitat_name):
    """
    Get Pokémon by habitat.
    
    Args:
        habitat_name: Name of the habitat
    
    Returns:
        List of Pokémon in that habitat
    """
    url = f"{BASE_URL}pokemon-habitat/{habitat_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return [p['name'] for p in data['pokemon_species']]
    except requests.RequestException as e:
        print(f"Error fetching habitat data: {e}")
        return []

def calculate_stat_with_iv_ev(base_stat, level=100, iv=31, ev=252, nature_modifier=1.0):
    """
    Calculate actual stat value with IVs, EVs, and nature.
    
    Args:
        base_stat: Base stat value
        level: Pokémon level (default 100)
        iv: Individual Value (0-31, default 31)
        ev: Effort Value (0-252, default 252)
        nature_modifier: Nature modifier (0.9, 1.0, or 1.1)
    
    Returns:
        Calculated stat value
    """
    # Formula for non-HP stats
    stat = int(((2 * base_stat + iv + (ev / 4)) * level / 100 + 5) * nature_modifier)
    return stat

def calculate_hp_with_iv_ev(base_hp, level=100, iv=31, ev=252):
    """
    Calculate HP stat value with IVs and EVs.
    
    Args:
        base_hp: Base HP value
        level: Pokémon level (default 100)
        iv: Individual Value (0-31, default 31)
        ev: Effort Value (0-252, default 252)
    
    Returns:
        Calculated HP value
    """
    # Formula for HP
    hp = int((2 * base_hp + iv + (ev / 4)) * level / 100 + level + 10)
    return hp

def get_pokemon_catch_rate_probability(catch_rate, current_hp_percent=1.0, status_bonus=1.0, ball_bonus=1.0):
    """
    Calculate catch probability.
    
    Args:
        catch_rate: Pokémon's catch rate
        current_hp_percent: Current HP as percentage (0.0 to 1.0)
        status_bonus: Status condition bonus (1.0 = none, 1.5 = paralyzed/burned/poisoned, 2.0 = sleep/freeze)
        ball_bonus: Poké Ball bonus (1.0 = regular, varies by ball type)
    
    Returns:
        Approximate catch probability percentage
    """
    # Simplified catch rate formula
    max_hp = 100
    current_hp = max_hp * current_hp_percent
    
    a = ((3 * max_hp - 2 * current_hp) * catch_rate * ball_bonus * status_bonus) / (3 * max_hp)
    
    if a >= 255:
        return 100.0
    
    # Shake probability
    b = 1048560 / (16711680 / a) ** 0.5
    shake_probability = b / 65536
    
    # Four shakes needed
    catch_probability = (shake_probability ** 4) * 100
    
    return min(100.0, catch_probability)

def get_nature_modifiers():
    """
    Get all Pokémon natures and their stat modifiers.
    
    Returns:
        Dictionary of natures and their effects
    """
    natures = {
        'Hardy': {'increased': None, 'decreased': None},
        'Lonely': {'increased': 'Attack', 'decreased': 'Defense'},
        'Brave': {'increased': 'Attack', 'decreased': 'Speed'},
        'Adamant': {'increased': 'Attack', 'decreased': 'Sp. Atk'},
        'Naughty': {'increased': 'Attack', 'decreased': 'Sp. Def'},
        'Bold': {'increased': 'Defense', 'decreased': 'Attack'},
        'Docile': {'increased': None, 'decreased': None},
        'Relaxed': {'increased': 'Defense', 'decreased': 'Speed'},
        'Impish': {'increased': 'Defense', 'decreased': 'Sp. Atk'},
        'Lax': {'increased': 'Defense', 'decreased': 'Sp. Def'},
        'Timid': {'increased': 'Speed', 'decreased': 'Attack'},
        'Hasty': {'increased': 'Speed', 'decreased': 'Defense'},
        'Serious': {'increased': None, 'decreased': None},
        'Jolly': {'increased': 'Speed', 'decreased': 'Sp. Atk'},
        'Naive': {'increased': 'Speed', 'decreased': 'Sp. Def'},
        'Modest': {'increased': 'Sp. Atk', 'decreased': 'Attack'},
        'Mild': {'increased': 'Sp. Atk', 'decreased': 'Defense'},
        'Quiet': {'increased': 'Sp. Atk', 'decreased': 'Speed'},
        'Bashful': {'increased': None, 'decreased': None},
        'Rash': {'increased': 'Sp. Atk', 'decreased': 'Sp. Def'},
        'Calm': {'increased': 'Sp. Def', 'decreased': 'Attack'},
        'Gentle': {'increased': 'Sp. Def', 'decreased': 'Defense'},
        'Sassy': {'increased': 'Sp. Def', 'decreased': 'Speed'},
        'Careful': {'increased': 'Sp. Def', 'decreased': 'Sp. Atk'},
        'Quirky': {'increased': None, 'decreased': None}
    }
    
    return natures

@lru_cache(maxsize=100)
def get_item_data(item_name):
    """
    Fetch item data from the API.
    
    Args:
        item_name: Name of the item
    
    Returns:
        Item data dictionary
    """
    url = f"{BASE_URL}item/{item_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching item data: {e}")
        return None

def batch_get_pokemon(pokemon_ids, delay=0.1):
    """
    Fetch multiple Pokémon with rate limiting.
    
    Args:
        pokemon_ids: List of Pokémon IDs or names
        delay: Delay between requests in seconds
    
    Returns:
        List of Pokémon data
    """
    pokemon_data = []
    
    for poke_id in pokemon_ids:
        data = get_pokemon_data(poke_id)
        if data:
            pokemon_data.append(data)
        time.sleep(delay)  # Rate limiting
    
    return pokemon_data

def get_type_color(type_name):
    """
    Get color code for a Pokémon type.
    
    Args:
        type_name: Name of the type
    
    Returns:
        Hex color code
    """
    type_colors = {
        'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0', 
        'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
        'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
        'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
        'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
        'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
    }
    
    return type_colors.get(type_name.lower(), '#777777')