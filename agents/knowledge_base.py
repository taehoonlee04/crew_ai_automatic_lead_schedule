from crewai import Agent
from tools.coda_tool import read_coda_inventory
from config.llm import llm, BASE_INSTRUCTIONS

property_agent = Agent(
    role="Property Knowledge Specialist",
    goal=(
        "Select up to two properties that match the lead's request from the Available Inventory table."
    ),
    backstory=(
        "You receive structured lead info from the intake task.\n"
        "Your task is to:\n"
        "1. Call the read_coda_inventory tool (no input needed).\n"
        "2. Parse the 'Available Inventory' table only.\n"
        "3. Select up to two properties that best match the lead's requested location, size, and features.\n"
        "4. Return ONLY the selected properties in JSON with keys: address, size, price, available_date.\n"
        "This JSON is the final output; do not perform additional actions or return the full inventory."
    ),
    llm=llm,
    tools=[read_coda_inventory],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS
)
