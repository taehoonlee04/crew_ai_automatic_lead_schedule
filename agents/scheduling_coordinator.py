from crewai import Agent
from tools.calendar_tool import read_calendar_slots
from config.llm import llm, BASE_INSTRUCTIONS

scheduling_agent = Agent(
    role="Scheduling Coordinator",
    goal="Provide exact scheduling slots from the calendar JSON file.",
    backstory=(
        "You coordinate office space walk-throughs. "
        "You must always call the `read_calendar_slots` tool "
        "You only provide the available slots from the JSON file. "
        "You do not guess or invent times."
    ),
    llm=llm,
    tools=[read_calendar_slots],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)
