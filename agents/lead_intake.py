from crewai import Agent
from tools.gmail_tool import read_gmail
from config.llm import llm, BASE_INSTRUCTIONS

email_agent = Agent(
    role="Lead Intake Specialist",
    goal="Read emails from leads and accurately summarize their request.",
    backstory=(
        "You handle the initial intake from Gmail. "
        "Your only responsibility is to extract the intent of the lead "
        "from the emails and make it clear for the next steps."
         "Read the email and extract:\n"
        "- 'Lead's name' from 'From' email id\n"
        "- 'Main request' from the 'Subject' and 'Body' of the email.\n"
        " Main request can be a request for property details, scheduling a tour, or both.\n"
        "- Desired property details (location, type, features)\n"
        "Extract this also from the 'Subject' and 'Body' of the email. There will be overlap with main request\n\n"
        "Return a clear intake summary."
    ),
    llm=llm,
    tools=[read_gmail],
    allow_delegation=False,
    verbose=True,
    instructions=BASE_INSTRUCTIONS,
)
