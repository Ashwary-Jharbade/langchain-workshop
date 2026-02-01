import json
from local_llm.core import getLLM, invoke_agent_and_stream_response
from langchain.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage, AIMessage

@tool
def getPokemonInfo(pokemon_name: str) -> str:
    """Get information about a specific Pokémon by name."""
    import requests
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        if response.status_code == 200:
            data = response.json()
            moves = data.get("moves", [])
            move_names = [move["move"]["name"] for move in moves]
            info = f"Pokemon Details In JSON: {", ".join(move_names)}"
            return info
        else:
            return "Pokémon not found."
    except Exception as e:
        return "Pokémon not found."

def getPokemonAttacks(name: str) -> str:
    llm = getLLM()
    pokemon_agent = llm.bind_tools([getPokemonInfo])
    messages = []
    messages.append(
        HumanMessage(content=name)
    )
    pokemon_response = pokemon_agent.invoke(messages)

    print("Tool Calls Made:", pokemon_response.tool_calls)

    if not pokemon_response.tool_calls:
        print("No attacks found.")
    else:
        for call in pokemon_response.tool_calls:
            result = getPokemonInfo.invoke(call["args"])
            messages.append(
                ToolMessage(
                    tool_call_id=call["id"],
                    content=str(result)
                )
            )
        messages.append(
            AIMessage(content=f"""
            Above is the information I found about {name} attacks.
            What are top attacks?
            Guardrails:
            If no attacks found say 'No attacks found.'
            If give name is not pokemon strictly say 'No attacks found. and do not add any more text.'
            Only respond with the attack names if available in numeric points line by line.
            Do not include any other information or generate information which is not available.
            Do not add additional text.
            """)
        )
        final_response = pokemon_agent.invoke(messages)
        print(final_response.content)

def getPokemonDetails():
    name = input("Enter the name of the Pokémon: ")
    getPokemonAttacks(name)

if __name__ == "__main__":
    getPokemonDetails()