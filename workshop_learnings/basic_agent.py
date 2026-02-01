from local_llm.core import getAgent

hr_agent = getAgent(
    system_prompt='You are a HR assistant, helping with employee queries and company policies.',
)

response = hr_agent.invoke({
    'message': 'What is the company policy on remote work?'
})

print(response)