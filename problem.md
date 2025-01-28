### Question:
Write a function that takes a pokemon as its input and outputs its evolutions, using the data from https://pokeapi.co/ to power your function.

### More details (for shorter interviews < 30 minutes to solve the problem)
The relevant APIs you will need to use are (see documentation here: https://pokeapi.co/docs/v2): 
1. Pokemon -> Pokemon Species (ex. https://pokeapi.co/api/v2/pokemon-species/charmander)
2. Evolution -> Evolution Chains (ex. https://pokeapi.co/api/v2/evolution-chain/2)

### More details about the input/outputs (provide these after giving the candidate a chance to tease out the requirements):
> Note: Make sure that you clarify the inputs and outputs right at the beginning of the interview. If they jump to the API, bring them back to make sure that they understand how pokemon evolutions work.

The output should be a list of pokemon names. If there are evolutions with multiple branches, the output should give just one of the evolution paths.

##### Examples (provide these simple examples if they need help):

1. Input: "charmander", Output: ["charmander", "charmeleon", "charizard"]
2. Input: "charizard", Output: ["charmander", "charmeleon", "charizard"]
3. Input: "eevee", Output: ["eevee", "vaporeon"]
    - Note: Other valid outputs include: ["eevee", "jolteon"], ["eevee", "flareon"], etc.
4. Input: "vaporeon", Output: ["eevee", "vaporeon"]
5. Input: "not a pokemon", Output: Error("The Pokemon does not exist")

### Solution:
See https://github.com/noam3j/pokeapi-interview-question/blob/main/solutions/python/simple-solution.py for a reference solution.

### Follow-up questions if there is time/ details about the scale
1. Caching - What if this function is called a lot of times. Can we do something to reduce the load on the pokemon API?
    - If time permitted, ask them to implement it. If no more time, just ask for an explanation
2. Testing (mocking API calls) - How would you write automated unit tests? 
    - If time permitted, ask them to implement it. If no more time, just ask for an explanation
3. DFS - Ideally, the path should include the pokemon from the input (see examples below). How would you write the code?
    - If time permitted, ask them to implement it.

##### More complicated examples (which requires dfs)
1. Input: "jolteon", Output: ["eevee", "jolteon"]
2. Input: "wurmple": ["wurmple", "silcoon", "beautifly"]
    - Note: This is also a valid output: ["wurmple", "cascoon", "dustox"] 
3. Input: "cascoon": ["wurmple", "cascoon", "dustox"]
4. Input: "dustox": ["wurmple", "cascoon", "dustox"]
5. Input: "silcoon": ["wurmple", "silcoon", "beautifly"]
6. Input: "beautifly": ["wurmple", "silcoon", "beautifly"]

### Follow-up solution:
See https://github.com/noam3j/pokeapi-interview-question/blob/main/solutions/python/follow-up-solution.py for a reference solution.

### Rubric:
TODO