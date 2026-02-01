import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from local_llm.core import getAgent, getLLM

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Evaluate the output correctness using a local LLM. It may not be 100% accurate.
def evaluateOutput(input, output):
    """Evaluate the output correctness using a local LLM."""
    llm = getLLM()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Evaluate if the output is correct for the given input. Respond with only 'Correct' or 'Incorrect'."),
        ("user", f"Input: {input}\nOutput: {output}")
    ])
    llm = prompt | llm
    response = llm.invoke({
        "input": input,
        "output": output
    })
    return response.content

def printEvaluation(query, output):
    print("-" * 40)
    print("Input:", query)
    evaluation = evaluateOutput(query, output)
    print("Output:", output.strip()[0:20] + ("..." if len(output) > 20 else ""))
    print("Evaluation:", evaluation)
    print("-" * 40)


async def main():
    mcp_client = MultiServerMCPClient(
        {
            "local-mcp-server": {
                'transport': "http",
                'url': 'http://localhost:8000/mcp'
            },
            "tavily-mcp-server": {
                'transport': "http",
                'url': f'https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}',
            }
        }
    )
    tools = await mcp_client.get_tools()
    agent = getAgent(tools=tools, verbose=True)
    query = "Add 4 + 15"
    response = await agent.ainvoke({
        "message": query
    })
    printEvaluation(query, response.content)


    query = "Why did USA attacked Venezuela?"
    response = await agent.ainvoke({
        "message": query
    })
    printEvaluation(query, response.content)


    async with mcp_client.session("local-mcp-server") as session:  
        # Pass the session to load tools, resources, or prompts
        resource_content = await session.read_resource("file://documents/dummy.txt")
        print("Resource Content:", resource_content.contents[0].text)

        prompts = await session.list_prompts()
        print("Available prompts:", prompts)

        tools = await load_mcp_tools(session)  
        agent = getAgent(tools=tools, verbose=True)
        query = "Add 10 + 25"
        response = await agent.ainvoke({
            "message": query
        })
        printEvaluation(query, response.content)

if __name__ == "__main__":
    asyncio.run(main())
