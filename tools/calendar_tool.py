import json
import os
from crewai_tools import tool

@tool("read_calendar_slots")
def read_calendar_slots() -> str:
    """Read available scheduling slots from calendar.json."""
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(parent_dir, "calendar.json")
    try:
        with open(json_path, "r") as f:
            calendar = json.load(f)
    except Exception as e:
        return f"Error reading calendar.json: {e}"
    return str(calendar.get("available_slots", []))

@tool("Read Gmail JSON")
def read_gmail(query: str) -> str:
    """Read Gmail leads stored in gmail.json and return messages containing the query."""
    import json, os

    parent_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(parent_dir)
    json_path = os.path.join(project_root, "gmail.json")
    print(f"Looking for gmail.json at: {json_path}")  # Debug print

    try:
        with open(json_path, "r") as f:
            emails = json.load(f)
    except Exception as e:
        return f"Error reading gmail.json: {e}"

    query_lower = query.lower()
    matches = [
        e for e in emails
        if any(query_lower in str(v).lower() for v in e.values())
    ]

    return str(matches) if matches else "No matching emails found."
