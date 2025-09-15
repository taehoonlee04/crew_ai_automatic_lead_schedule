import logging
from crewai import Crew, Process
from agents.schedule import scheduling_agent
from agents.lead_intake import email_agent
from agents.knowledge_base import property_agent
from tasks.lead_reply_task import intake_task, property_task, scheduling_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main() -> None:
    crew = Crew(
        agents=[email_agent, property_agent, scheduling_agent],
        tasks=[intake_task, property_task, scheduling_task],
        verbose=True,
    )
    try:
        result = crew.kickoff()
        logging.info("=== FINAL OUTPUT ===\n%s", result)
    except Exception as e:
        logging.error("Crew execution failed: %s", e)

if __name__ == "__main__":
    main()