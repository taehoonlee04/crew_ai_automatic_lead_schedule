import json
from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_community.chat_models import ChatOllama
# Load environment variables (if any)
load_dotenv()

# === LLM CONFIGURATION ===
ollama_llm = ChatOllama(
    model="mistral",
    temperature=0,              # Deterministic, no creative wandering
    num_predict=512             # Control max output length
)

# === TOOLS ===

@tool("Read Gmail JSON")
def read_gmail(query: str) -> str:
    """Read Gmail leads stored in gmail.json and return messages containing the query."""
    with open("gmail.json", "r") as f:
        emails = json.load(f)
    matches = [e for e in emails if query.lower() in e["body"].lower()]
    return str(matches) if matches else "No matching emails found."


@tool("Read Property Info from Coda JSON")
def read_property_info(property_name: str) -> str:
    """Fetch property information from coda.json by property name."""
    with open("coda.json", "r") as f:
        properties = json.load(f)
    return str(properties.get(property_name.lower().replace(" ", "_"), "Property not found."))


@tool("Read Available Calendar Slots")
def read_calendar_slots(_: str) -> str:
    """Read available scheduling slots from calendar.json."""
    with open("calendar.json", "r") as f:
        calendar = json.load(f)
    return str(calendar.get("available_slots", []))

# === AGENTS ===
# Baseline instruction applied across all agents:
BASE_INSTRUCTIONS = (
    "Always use the provided tools to answer. "
    "Never hallucinate information. "
    "If information is missing, clearly state what is missing. "
    "Do not make assumptions. "
    "Be concise, professional, and structured in responses."
)

email_agent = Agent(
    role="Email Intake Specialist",
    goal="Read new emails from leads and accurately summarize their request.",
    backstory=(
        "You handle the initial intake of leads from Gmail. "
        "Your only responsibility is to extract the intent of the lead "
        "from the emails and make it clear for the next steps."
    ),
    llm=ollama_llm,
    tools=[read_gmail],
    allow_delegation=True,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)

property_agent = Agent(
    role="Property Knowledge Specialist",
    goal="Fetch precise property information from the Coda JSON file without deviation.",
    backstory=(
        "You maintain accurate, up-to-date property details from the knowledge base. "
        "You must only return factual data from the JSON, never fabricate."
    ),
    llm=ollama_llm,
    tools=[read_property_info],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)

scheduling_agent = Agent(
    role="Scheduling Coordinator",
    goal="Provide exact scheduling slots from the calendar JSON file.",
    backstory=(
        "You coordinate office space walk-throughs. "
        "You only provide the available slots from the JSON file. "
        "You do not guess or invent times."
    ),
    llm=ollama_llm,
    tools=["Read Available Calendar Slots"],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)

# === TASK ===

lead_email_task = Task(
    description=(
        "1. The Email Intake Specialist must read emails containing 'downtown office'.\n"
        "2. The Property Knowledge Specialist must fetch info about the 'downtown office'.\n"
        "3. The Scheduling Coordinator must provide available tour slots.\n"
        "4. Together, draft a professional reply email to the lead with property details and available tour times.\n\n"
        "⚠️ Important: The reply must only include facts from the JSON files. "
        "If any info is missing, explicitly state that it is unavailable."
    ),
    agent=email_agent,
    expected_output=(
        "Drafted professional email responses for each lead. "
        "Responses must include accurate property details (from JSON only), "
        "polite tone, and next-step guidance (e.g., scheduling a tour)."
    ),
    max_steps=5
)

# === CREW ===
crew = Crew(
    agents=[email_agent, property_agent, scheduling_agent],
    tasks=[lead_email_task],
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== FINAL OUTPUT ===")
    print(result)
