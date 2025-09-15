from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

# Create a single OpenAI client
client = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


BASE_INSTRUCTIONS = (
    "Always use the provided tools to answer. "
    "Never hallucinate information. "
    "If information is missing, clearly state what is missing. "
    "Do not make assumptions. "
    "Be concise, professional, and structured in responses."
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    max_tokens=512,
)