import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def get_pokemon_data(pokemon_name_or_id):
    """Fetches data for a given Pokémon by name or ID."""
    url = f"{BASE_URL}pokemon/{pokemon_name_or_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise HTTP errors
        return response.json()
    except requests.RequestException as e:
        print("Error fetching Pokémon data:", e)
        return None

def get_pokemon_species_data(pokemon_name_or_id):
    """Fetches species data including evolution chain for a Pokémon."""
    try:
        species_url = f"{BASE_URL}pokemon-species/{pokemon_name_or_id}"
        species_response = requests.get(species_url, timeout=5)
        species_response.raise_for_status()

        evo_chain_url = species_response.json()["evolution_chain"]["url"]
        evo_chain_response = requests.get(evo_chain_url, timeout=5)
        evo_chain_response.raise_for_status()

        chain = []
        def traverse(node):
            chain.append(node["species"]["name"])
            for evo in node.get("evolves_to", []):
                traverse(evo)

        traverse(evo_chain_response.json()["chain"])
        return chain
    except requests.RequestException as e:
        print("Error fetching evolution chain:", e)
        return []
    except KeyError as e:
        print("Unexpected JSON structure:", e)
        return []