import json
import os
from crewai_tools import tool

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
    if query_lower:
        matches = [
            e for e in emails
            if any(query_lower in str(v).lower() for v in e.values())
        ]
    else:
        matches = emails

    # Build a clean summary string
    summary_lines = []
    for i, email in enumerate(matches, 1):
        summary_lines.append(
            f"--- Match {i} ---\n"
            f"From: {email.get('from','')}\n"
            f"Subject: {email.get('subject','')}\n"
            f"Body: {email.get('body','')}\n"
        )
    return "\n".join(summary_lines)