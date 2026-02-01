from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import ToolMessage, AIMessageChunk, AIMessage, BaseMessage, HumanMessage, SystemMessage

def getLLM(model="", streaming=False, temperature=0.7):
    return ChatOllama(
            model="deepseek-r1:7b" if model == "deepseek" else "qwen2.5:7b",  
            base_url="http://localhost:11434",
            temperature=temperature,
            streaming=streaming,
        )

def normalize_to_messages(x):
    # Case 1: streaming chunk → full AIMessage
    if isinstance(x, AIMessageChunk):
        return [AIMessage(content=x.content)]

    # Case 2: single AIMessage
    if isinstance(x, BaseMessage):
        return [x]

    # Case 3: already a list of messages
    if isinstance(x, list):
        return x

    # Case 4: raw string
    if isinstance(x, str):
        return [AIMessage(content=x)]

    raise ValueError(f"Unsupported type passed to LLM: {type(x)}")


def getAgent(system_prompt="", model="", streaming=True, temperature=0.7, tools=[], verbose=False):

    async def call_tool(message):
        if isinstance(message, AIMessageChunk):
            message = AIMessage(content=message.content)
        
        if not message.tool_calls:
            return message
        
        # No tool calls → return message as-is
        if not getattr(message, "tool_calls", None):
            return message

        tool_map = {tool.name: tool for tool in tools}
        messages = [message]
        for call in message.tool_calls:
            tool = tool_map[call["name"]]
            result = await tool.ainvoke(call["args"])

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"]
                )
            )
        messages.append(
            SystemMessage(content="Tool calls completed. Continue generating the final response. Do not deviate from the tool response and only use the tool response and do not add extra text apart from tool response.")
        )
        if verbose:
            print("Tool invocation:", message.tool_calls)
        return messages


    llm = getLLM(model=model, streaming=streaming, temperature=temperature)
    llm_with_tools = llm.bind_tools(tools)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{message}"),
        ]
    )
    if not system_prompt:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{message}"),
            ]
        )
        
    agent = (
        RunnablePassthrough()
        | prompt
        | llm_with_tools
        | RunnableLambda(call_tool)
        | RunnableLambda(normalize_to_messages)
        | llm
    )
    return agent

def invoke_agent_and_stream_response(agent, message):
    for chunk in agent.stream(message):
        print(chunk.content, end="", flush=True)
    print()