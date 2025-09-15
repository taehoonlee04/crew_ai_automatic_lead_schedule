import os
import json
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
CODA_API_KEY = os.getenv("CODA_API_KEY")

DOC_ID = "dXjVBxN9zV_"      # from your link
TABLE_ID = "su8O28Dk"       # Available Inventory table
CACHE_FILE = "coda.json"

HEADERS = {"Authorization": f"Bearer {CODA_API_KEY}"}

def fetch_coda_inventory():
    """Fetch inventory table from Coda API and cache it locally."""
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

    data = response.json()

    # Convert into simple dict {property_name: property_data}
    inventory = {}
    for row in data.get("items", []):
        cells = {c["column"]: c["value"] for c in row["values"]}
        name = str(cells.get("property_name", "")).lower().replace(" ", "_")
        inventory[name] = cells

    with open(CACHE_FILE, "w") as f:
        json.dump(inventory, f, indent=2)

    print(f"✅ Cached {len(inventory)} properties to {CACHE_FILE}")


def read_property_info(property_name: str) -> dict:
    """Read property info from cached coda.json by property name."""
    if not os.path.exists(CACHE_FILE):
        raise FileNotFoundError("Cache not found. Run fetch_coda_inventory() first.")

    with open(CACHE_FILE, "r") as f:
        inventory = json.load(f)

    key = property_name.lower().replace(" ", "_")
    return inventory.get(key, {"error": "Property not found."})


if __name__ == "__main__":
    # Step 1: Fetch latest data from Coda
    fetch_coda_inventory()

    # Step 2: Example: Read "Downtown Office"
    property_name = "Downtown Office"
    info = read_property_info(property_name)
    print(f"\n📍 Info for {property_name}:\n{json.dumps(info, indent=2)}")
