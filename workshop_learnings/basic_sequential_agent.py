import os
import asyncio
from langchain.messages import HumanMessage
from local_llm.core import getLLM, getAgent
from dotenv import load_dotenv
load_dotenv()

# Writer Agent 
writer_agent = getAgent(
    system_prompt="You are a creative writer with working experience in Top Media Company",
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
            "message": f"Please write a detailed article on the topic in 100 words: '{topic}'"
        }
    )

    written_content = writer_result.content

    print("Written Content:", written_content)

    print("=== Writer Agent's Output Delivered to Editor Agent ===")

    # Step 2: Editor Agent refines content
    editor_result = await editor_agent.ainvoke(
        {
            "message": f"Please refine the following article in 100 words: '{written_content}'"
        }
    )

    print("Refined Content:", editor_result)

    refined_content = editor_result.content

    print("=== Editor Agent Output is Ready and Delivered ===")
    return {
      "topic": topic,
      "draft": written_content,
      "final": refined_content
    }

async def main():
    topic = "The Future of Artificial Intelligence in Everyday Life"
    result = await run_sequential_pipeline(topic)

    print("\n=== Final Output ===")
    print(f"Topic: {result['topic']}\n")

    print("Draft Content:\n")
    print(result['draft'])

    print("\nRefined Content:\n")
    print(result['final'])  

if __name__ == "__main__":
    asyncio.run(main())
