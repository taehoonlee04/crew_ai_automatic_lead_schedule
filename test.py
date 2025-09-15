# crew_script.py
from crewai import Crew, Task
from agents.lead_intake import email_agent

crew = Crew(
    agents=[email_agent],
    tasks=[
        Task(
            description="tell me the lead emails",
            agent=email_agent,
            expected_output="an email reply",
            max_steps=1
        )
    ],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("Result:", result)
