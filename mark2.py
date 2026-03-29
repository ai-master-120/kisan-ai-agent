from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGroq(
    api_key="YOUR_API_KEY",
    model="llama-3.3-70b-versatile",
    temperature=0.6
)

messages = [
    SystemMessage(content="""You are an expert agricultural advisor for Indian farmers. 
    You give practical, simple advice about crops, soil, weather, and farming.
    Always give advice specific to Indian farming conditions."""),

    HumanMessage(content="My soil is dry and its winter in Punjab. What crop should I grow?")
]

response = llm.invoke(messages)
print(response.content)