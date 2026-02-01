import os
import asyncio
from langchain.messages import HumanMessage
from local_llm.core import getLLM, getAgent
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

tavily_tool = TavilySearch(
    max_results=10,
    topic="general",
    search_depth="advanced",  # Use advanced for better research quality
    api_key=os.getenv("TAVILY_API_KEY")
)

# Writer Agent 
writer_agent = getAgent(
    system_prompt="""You are a creative writer with working experience in Top Media Company. 
    You have access to web search capabilities. Before writing, use the search tool to 
    research the topic thoroughly to ensure accuracy and include latest information.""",
    tools=[tavily_tool],  # Add the search tool
    verbose=True
)

print("Writer Agent created successfully.")

# Editor Agent 
editor_agent = getAgent(
    system_prompt="You are a meticulous editor, skilled at refining and enhancing written content",
)

print("Editor Agent created successfully.")


# defining sequential interaction between Writer and Editor agents
async def run_sequential_pipeline(topic: str): 
    """
    Sequential multi-agent pipeline.
    1) Writer agent creates content on a given topic
    2) Editor agent refines that content.
    """
    print(f"Topic: {topic}\n")
    
    # Step 1: Writer Agent creates content
    writer_result = await writer_agent.ainvoke(
        {
            "message": f"""Please research on web and write a detailed article on: '{topic}'
                    
                    Instructions:
                    1. First, search for latest information and trends about this topic
                    2. Then write a comprehensive article incorporating your research
                    3. Include relevant facts, statistics, and current developments
                    4. Do not exceed 300 words
                    5. Do not ask for any clarifications, just produce the article based on your research
                """
        }
    )

    written_content = writer_result.content

    print("Written Content:", written_content)

    print("=== Writer Agent's Output Delivered to Editor Agent ===")

    # Step 2: Editor Agent refines content
    editor_result = await editor_agent.ainvoke(
        {
            "message": f"""Please refine and enhance the following article:
                    Topic: '{topic}'
                    
                    {written_content}
                    
                    Focus on:
                    - Clarity and flow
                    - Grammar and style
                    - Structure and readability
                    - Fact consistency
                    - Engaging language
                    - Conciseness
                    - Do not exceed the original content length
                    - Do not ask for any clarifications, just produce the article based on your research
                """
        }
    )
    refined_content = editor_result.content

    print("Refined Content:", refined_content)

    print("=== Editor Agent Output is Ready and Delivered ===")
    return {
      "topic": topic,
      "draft": written_content,
      "final": refined_content
    }

async def main():
    topic = "The odds of Humans Colonizing Mars in the Next 50 Years"
    result = await run_sequential_pipeline(topic)

    print("\n=== Final Output ===")
    print(f"Topic: {result['topic']}\n")

    print("Draft Content:\n")
    print(result['draft'])

    print("\nRefined Content:\n")
    print(result['final'])  

if __name__ == "__main__":
    asyncio.run(main())
