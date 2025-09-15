from crewai import Task
from agents.lead_intake import email_agent
from agents.knowledge_base import property_agent
from agents.schedule import scheduling_agent

# 1️⃣ Intake Task - Email Agent
intake_task = Task(
    description=(
        "Fetch new lead emails from Gmail and extract structured details. "
        "Use the Read Gmail JSON tool to search for relevant emails.\n\n"
        "Then parse the email(s) and return a JSON object with the following fields:\n"
        "  - lead_name\n"
        "  - main_request\n"
        "  - desired_property_details (location, type, features)"
    ),
    agent=email_agent,
    expected_output= "A JSON object containing the extracted lead details, for example:\n"
        "{\n"
        '  "lead_name": "Jimmy Fallon",\n'
        '  "main_request": "Office space inquiry",\n'
        '  "desired_property_details": "2000sqft office on Bluegrass Parkway"\n'
        "}"
)

# 2️⃣ Property Lookup Task - Property Agent
property_task = Task(
    description=(
        "Using the intake summary, look up up to two matching properties in coda.json. "
        "Return details such as address, square footage, price, and key features."
    ),
    agent=property_agent,
    expected_output="Property details for up to two matching properties.",
    context=[intake_task]   # depends on intake task
)

# 3️⃣ Scheduling & Reply Task - Scheduling Agent
scheduling_task = Task(
    description=(
        "Using the property details, provide the Google Calendar booking link for tour scheduling. "
        "Return 2–3 possible booking options for the lead.\n\n"
        "Finally, draft a professional reply email to the lead that:\n"
        "- Acknowledges their inquiry\n"
        "- Presents up to two property options\n"
        "- Suggests available tour times\n"
        "- Includes a booking link for confirmation"
    ),
    agent=scheduling_agent,
    expected_output="Final polished email reply with properties, tour times, and booking link.",
    context=[property_task]   # depends on property lookup
)
