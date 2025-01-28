from abc import ABC, abstractmethod
import requests
from collections import deque
from typing import List

POKEAPI_V2_URL = "https://pokeapi.co/api/v2/"

class PokemonApiClient(ABC):

    @abstractmethod
    def get_pokemon_species(self, spieces_id: str) -> dict:
        pass

    @abstractmethod
    def get_evolution_chain(self, url: str) -> dict:
        pass


class RealPokemonApiClient(ABC):
    def get_pokemon_species(self, spieces_name: str) -> dict:
        response = requests.get(f"{POKEAPI_V2_URL}/pokemon-species/{spieces_name}")
        
        if response.status_code != 200:
            raise ValueError("The Pokemon does not exist")

        return response.json()

    def get_evolution_chain(self, url: str) -> dict:
        return requests.get(url).json()


class MockPokemonApiClient(ABC):
    def get_pokemon_species(self, spieces_name: str) -> dict:
        if spieces_name in {"charmander", "charmeleon", "charizard"}:
            return {
                "evolution_chain": {
                    "url": "https://pokeapi.co/api/v2/evolution-chain/2/"
                }
            }
        elif spieces_name in {"eevee", "jolteon", "vaporeon"}:
            return {
                "evolution_chain": {
                    "url": "https://pokeapi.co/api/v2/evolution-chain/67/"
                }
            }
        elif spieces_name in {"wurmple", "cascoon", "dustox", "silcoon", "beautifly"}:
            return {
                "evolution_chain": {
                    "url": "https://pokeapi.co/api/v2/evolution-chain/135/"
                }
            }
        
        raise ValueError("The Pokemon does not exist")

    def get_evolution_chain(self, url: str) -> dict:
        if url == "https://pokeapi.co/api/v2/evolution-chain/2/":
            return {
                "chain": {
                    "species": {"name": "charmander"},
                    "evolves_to": [
                        {
                            "species": {"name": "charmeleon"},
                            "evolves_to": [
                                {"species": {"name": "charizard"}, "evolves_to": []}
                            ],
                        }
                    ],
                }
            }
        elif url == "https://pokeapi.co/api/v2/evolution-chain/67/":
            return {
                "chain": {
                    "species": {"name": "eevee"},
                    "evolves_to": [
                        {
                            "species": {
                                "name": "vaporeon",
                            },
                            "evolves_to": [],
                        },
                        {
                            "species": {
                                "name": "jolteon",
                            },
                            "evolves_to": [],
                        },
                    ],
                }
            }
        elif url == "https://pokeapi.co/api/v2/evolution-chain/135/":
            return {
                "chain": {
                    "species": {"name": "wurmple"},
                    "evolves_to": [
                        {
                            "species": {
                                "name": "silcoon",
                            },
                            "evolves_to": [
                                {
                                    "species": {
                                        "name": "beautifly",
                                    },
                                    "evolves_to": []
                                }
                            ],
                        },
                        {
                            "species": {
                                "name": "cascoon",
                            },
                            "evolves_to": [
                                {
                                    "species": {
                                        "name": "dustox",
                                    },
                                    "evolves_to": []
                                }
                            ],
                        },
                    ],
                }
            }

class PokemonAdapter:

    def __init__(self, pokemon_api_client: PokemonApiClient):
        self.pokemon_api_client = pokemon_api_client
        self.evolutions_cache = {}

    def get_evolutions(self, name: str) -> List[str]:
        name = name.lower()
        evolution_chain = self._get_evolution_chain(name)
        return self._parse_evolution_chain(name, evolution_chain)

    def _parse_evolution_chain(self, target_name: str, evolution_chain: dict):

        evolutions: List[str] = deque([])

        def search_for_pokemon_rec(curr_pokemon: dict):

            curr_name = curr_pokemon["species"]["name"]
            evolutions.append(curr_name)

            if target_name == curr_name:
                return curr_pokemon

            # loop through all evolutions until we find the path that has the target pokemon
            for evolution in curr_pokemon["evolves_to"]:
                found = search_for_pokemon_rec(evolution)
                if found:
                    return found

            # if we get here, it means we went down an incorrect path, which did not have the target
            # pokemon, so we need to remove this pokemon from the list of evolutions
            evolutions.pop()

            return None

        def continue_chain(curr_pokemon: dict):
            if curr_pokemon["evolves_to"]:

                # Pick the first evolution (any will work)
                evolution = curr_pokemon["evolves_to"][0]
                evolutions.append(evolution["species"]["name"])
                continue_chain(evolution)

        curr_pokemon = evolution_chain["chain"]
        curr_pokemon = search_for_pokemon_rec(curr_pokemon)
        continue_chain(curr_pokemon)

        return evolutions

    def _get_evolution_chain(self, name: str) -> dict:

        if name in self.evolutions_cache:
            return self.evolutions_cache[name]

        species = self.pokemon_api_client.get_pokemon_species(name)
        evolutions = self.pokemon_api_client.get_evolution_chain(
            species["evolution_chain"]["url"]
        )

        self.evolutions_cache[name] = evolutions

        return evolutions


# Mock implementation
if __name__ == "__main__":

    # pokemon_api_client = RealPokemonApiClient()
    pokemon_api_client = MockPokemonApiClient()
    pokemon_adapter = PokemonAdapter(pokemon_api_client)

    def print_evolutions(name: str):
        try:
            print(f"'{name}': {pokemon_adapter.get_evolutions(name)}")
        except ValueError as e:
            print(f"'{name}': {e}")

    print_evolutions("charmander")
    print_evolutions("charmeleon")
    print_evolutions("charizard")
    print_evolutions("eevee")
    print_evolutions("vaporeon")
    print_evolutions("jolteon")
    print_evolutions("wurmple")
    print_evolutions("cascoon")
    print_evolutions("dustox")
    print_evolutions("silcoon")
    print_evolutions("beautifly")
    print_evolutions("not a pokemon")
