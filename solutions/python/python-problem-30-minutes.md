For python users in a 30 minute call, the following information should be given:

```python
"""
Write a function that takes a pokemon as its input and outputs its evolutions, using the data from https://pokeapi.co/ to power your function.

Most pokemon have one evolution chain (e.g. charmander). However, there are some pokemon that have multiple (can evolve into many different pokemon) (e.g. eevee). You only need to return one chain of evolutions.

Example input: charmander
Example output: charmander -> charmeleon -> charizard

The relevant APIs you will need to use are:
1. Pokemon -> Pokemon Species (ex. https://pokeapi.co/api/v2/pokemon-species/charmander) 
2. Evolution -> Evolution Chains (ex. https://pokeapi.co/api/v2/evolution-chain/2)

You can also try out some API calls and see formatted data here: https://pokeapi.co/

To make API calls in Python, you can reference the "requests" documentation here: https://pypi.org/project/requests/

Here are a few more examples:

| # | Input      | Expected output                         |
| - | ---------  | --------------------------------------- |
| 1 | charmander | charmander -> charmeleon -> charizard   |
| 2 | charmeleon | charmander -> charmeleon -> charizard   |
| 3 | charizard  | charmander -> charmeleon -> charizard   |
| 4 | eevee      | eevee -> vaporeon (or eevee -> jolteon) |
| 5 | vaporeon   | eevee -> vaporeon                       |
| 6 | jolteon    | eevee -> jolteon                        |

Explanation:

1/2/3. The charmander/charmeleon/charizard evolution chain is simple. It is not one of the examples of evolution chains that has multiple branching evolutions.
4. The eevee evolution chain is an example of branching evolutions - it can either evolve into vaporeon or jolteon. If the input is "eevee", we don't care whether the output is "eevee -> vaporeon" or "eevee -> jolteon".
5. Because the input is "vaporeon", the output must contain "vaporeon".
6. Because the input is "jolteon", the output must contain "jolteon".
"""
```
