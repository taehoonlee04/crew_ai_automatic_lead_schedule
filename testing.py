# Load environment variables from .env
from dotenv import load_dotenv
import os
import requests

load_dotenv()
print("Loaded API key:", os.getenv("CODA_PROPERTY_API_KEY"))

# Load your Coda API key
CODA_API_KEY = os.getenv("CODA_PROPERTY_API_KEY")
DOC_ID = "XjVBxN9zV_"  # Remove trailing spaces
PAGE_ID = "su8O28Dk"   # From Inventory_su8O28Dk
SECTION_ID = "_lugC-wEG"  # After the # in URL

if not CODA_API_KEY:
    raise Exception("Coda API key not found. Make sure CODA_API_KEY is set in your .env file.")

# FIX: Use f-strings with f prefix, or use .format(), or use % formatting
headers = {"Authorization": f"Bearer {CODA_API_KEY}"}  # ✅ Correct with f-string
print("Using token:", CODA_API_KEY[:6] + "..." + CODA_API_KEY[-4:])

# FIX: Use f-string here too
url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables"  # ✅ Correct with f-string

print(f"Making request to: {url}")
print(f"With headers: {headers}")

response = requests.get(url, headers=headers)

print(f"Response status: {response.status_code}")
print(f"Response headers: {dict(response.headers)}")

if response.status_code == 401:
    print("Raw response text:", response.text)
    raise Exception("Unauthorized: Check that your API key is correct and has access to this doc.")
elif response.status_code == 404:
    raise Exception("Doc not found: Check that DOC_ID is correct and your account has access to it.")
elif response.status_code != 200:
    raise Exception(f"Failed to fetch tables: {response.status_code}, {response.text}")

tables = response.json().get("items", [])
if not tables:
    print("No tables found in the doc.")
else:
    print("Tables in the doc:")
    for table in tables:
        print(f"- {table['name']} (id: {table['id']})")