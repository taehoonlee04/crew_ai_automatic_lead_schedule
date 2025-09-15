# tasks/run_scheduling_task.py
from crewai import Task
from agents.schedule import scheduling_agent

calendar_task = Task(
    description="Fetch and return available Google Calendar slots.",
    agent=scheduling_agent,
    expected_output="List of available slots",
    max_steps=1
)
