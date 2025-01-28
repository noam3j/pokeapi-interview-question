import requests
from typing import List

POKEAPI_V2_URL = "https://pokeapi.co/api/v2/"

def get_evolutions(name: str) -> List[str]:
    name = name.lower()

    response = requests.get(f"{POKEAPI_V2_URL}/pokemon-species/{name}")

    if response.status_code != 200:
            raise ValueError("The Pokemon does not exist")
        
    species = response.json()

    evolution_chain = requests.get(species["evolution_chain"]["url"]).json()

    evolutions = []

    curr_pokemon = evolution_chain["chain"]

    while curr_pokemon:
        evolutions.append(curr_pokemon["species"]["name"])
        evolves_to = curr_pokemon["evolves_to"]

        if not evolves_to:
            curr_pokemon = None
        else:
            next_evolution = evolves_to[0]
            curr_pokemon = next_evolution

    return evolutions

if __name__ == "__main__":

    def print_evolutions(name: str):
        try:
            print(f"'{name}': {get_evolutions(name)}")
        except ValueError as e:
            print(f"'{name}': {e}")

    print_evolutions("charmander")
    print_evolutions("charmeleon")
    print_evolutions("charizard")
    print_evolutions("eevee")
    print_evolutions("vaporeon")
    print_evolutions("jolteon") # gives the incorrect answer
    print_evolutions("wurmple")
    print_evolutions("cascoon") # gives the incorrect answer
    print_evolutions("dustox") # gives the incorrect answer
    print_evolutions("silcoon")
    print_evolutions("beautifly")
    print_evolutions("not a pokemon")