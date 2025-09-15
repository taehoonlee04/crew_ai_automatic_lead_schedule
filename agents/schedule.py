from crewai import Agent
from crewai_tools import tool
from tools.google_calendar_tool import provide_booking_link
from config.llm import llm, BASE_INSTRUCTIONS

scheduling_agent = Agent(
    role="Scheduling Coordinator",
    goal="Give leads the Google Calendar booking link so they can schedule their own tours.",
    backstory=(
        "You ONLY call the 'Provide Booking Link' tool, without any inputs"
        "and craft a warm, personable email reply with the returned link directly with the client."
        "Assume Client name from the email is the name to use in greeting."
        "Always in include signature at the end of the email. Taehoon Lee, Assistant to the regional manager, 502-111-8282"
        "within the email, hyperlink the text 'booking link' to the actual booking link URL."
    ),
    llm=llm,
    tools=[provide_booking_link],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)
