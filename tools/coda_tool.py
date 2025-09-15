import os
import requests
import json
import datetime
from dotenv import load_dotenv
from crewai_tools import tool

# Load environment variables
load_dotenv()

# Configuration from your URL: https://coda.io/d/Leasing-Center-2-0_dXjVBxN9zV_/Inventory_su8O28Dk#_lugC-wEG
CODA_API_KEY = os.getenv("CODA_API_KEY")
DOC_ID = "XjVBxN9zV_"  # Remember: removed 'd' prefix
PAGE_ID = "su8O28Dk"   # From Inventory_su8O28Dk
SECTION_ID = "_lugC-wEG"  # After the # in URL

# Direct table references
INVENTORY_TABLES = {
    "Available Inventory": "table-LU9xcQpu3o",
    "Unavailable Inventory": "table-Gj2Fr0EINb"
}

def get_coda_headers():
    """Get headers for Coda API requests"""
    if not CODA_API_KEY:
        raise Exception("CODA_API_KEY not found in environment variables")
    return {"Authorization": f"Bearer {CODA_API_KEY}"}

@tool("read_coda_inventory")
def read_coda_inventory() -> str:
    """
    Fetch inventory data from the Coda document's Available and Unavailable Inventory tables.
    Returns property/unit data for the AI agent to use in scheduling and management.
    """

    try:
        headers = get_coda_headers()
        inventory_data = {}

        # Get data from both inventory tables
        for table_name, table_id in INVENTORY_TABLES.items():
            print(f"DEBUG: Fetching data from '{table_name}' (ID: {table_id})")

            # Fetch rows from this table
            rows_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{table_id}/rows"
            rows_response = requests.get(rows_url, headers=headers)

            if rows_response.status_code == 200:
                rows_data = rows_response.json()
                rows = rows_data.get("items", [])

                print(f"DEBUG: Table '{table_name}' has {len(rows)} rows")

                # Process the rows to extract useful data
                processed_rows = []
                for row in rows:
                    row_data = {
                        "row_id": row.get("id"),
                        "values": {}
                    }

                    # Extract cell values
                    values = row.get("values", {})
                    for column_id, cell_data in values.items():
                        # Try to get readable column name
                        display_value = cell_data
                        if isinstance(cell_data, dict):
                            display_value = cell_data.get("displayValue", cell_data.get("value", str(cell_data)))

                        row_data["values"][column_id] = display_value

                    processed_rows.append(row_data)

                # Also get column information for better data interpretation
                columns_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{table_id}/columns"
                columns_response = requests.get(columns_url, headers=headers)

                columns_info = []
                if columns_response.status_code == 200:
                    columns_data = columns_response.json()
                    columns_info = columns_data.get("items", [])
                    print(f"DEBUG: Table '{table_name}' has {len(columns_info)} columns")

                inventory_data[table_name] = {
                    "table_id": table_id,
                    "total_rows": len(rows),
                    "rows": processed_rows,
                    "columns": columns_info
                }
            else:
                print(f"DEBUG: Failed to fetch rows from table '{table_name}': {rows_response.status_code}")
                inventory_data[table_name] = {
                    "error": f"Failed to fetch data: {rows_response.status_code}",
                    "error_details": rows_response.text,
                    "table_id": table_id
                }

        # Get page info
        page_info = {}
        try:
            page_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/pages/{PAGE_ID}"
            page_response = requests.get(page_url, headers=headers)
            if page_response.status_code == 200:
                page_data = page_response.json()
                page_info = {
                    "name": page_data.get("name"),
                    "type": page_data.get("type"),
                    "id": page_data.get("id")
                }
        except Exception as e:
            print(f"DEBUG: Could not fetch page info: {e}")

        result = {
            "source": "Coda Inventory Page",
            "doc_id": DOC_ID,
            "page_id": PAGE_ID,
            "page_info": page_info,
            "inventory_data": inventory_data,
            "tables_processed": list(INVENTORY_TABLES.keys()),
            "timestamp": str(datetime.datetime.now())
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "error": f"Failed to read Coda inventory data: {str(e)}",
            "error_type": type(e).__name__,
            "config": {
                "doc_id": DOC_ID,
                "page_id": PAGE_ID,
                "section_id": SECTION_ID,
                "tables": INVENTORY_TABLES
            }
        })

# Standalone function for direct use (not as a tool)
def get_inventory_data_direct():
    """Direct function to get inventory data without CrewAI tool wrapper"""
    headers = get_coda_headers()

    print("Fetching data from specified inventory tables:")
    for table_name, table_id in INVENTORY_TABLES.items():
        print(f"  - {table_name} (ID: {table_id})")

    inventory_data = {}

    for table_name, table_id in INVENTORY_TABLES.items():
        print(f"\n{'='*60}")
        print(f"FETCHING: {table_name}")
        print(f"{'='*60}")

        # Manual column mapping based on observed data patterns
        manual_column_mapping = {
            "c-an7SE9JACl": "Address",
            "c-xdgenU-uvl": "Suite No.",
            "c-3UMTwnyNCJ": "Use",
            "c-Z02gN1B7zi": "RSF",
            "c-ZZQp_OmMfe": "Photos/Drawings",
            "c-JehWcK4QvA": "Available Starting",
            "c-rMqD5hhEY9": "Current Active Deals",
            "c-hMyF6HLGgQ": "Notes",
            "c-r5FRDTpppF": "Unknown Field",
            "c-okOwndwr3T": "Status"
        }

        # Try to get column information from API first
        columns_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{table_id}/columns"
        print(f"DEBUG: Attempting to fetch columns from API...")
        columns_response = requests.get(columns_url, headers=headers)

        column_mapping = {}
        if columns_response.status_code == 200:
            columns_data = columns_response.json()
            columns = columns_data.get("items", [])
            print(f"✓ API returned {len(columns)} columns")

            # Create mapping from column ID to column name
            for column in columns:
                column_id = column.get("id")
                column_name = column.get("name", column_id)
                column_mapping[column_id] = column_name

            print("✓ Using API column mapping")
        else:
            print(f"✗ API columns failed ({columns_response.status_code}), using manual mapping")
            column_mapping = manual_column_mapping

        print(f"Final column mapping ({len(column_mapping)} columns):")
        for col_id, col_name in column_mapping.items():
            print(f"  {col_id} -> {col_name}")

        # Get table row data
        rows_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{table_id}/rows"
        rows_response = requests.get(rows_url, headers=headers)

        if rows_response.status_code == 200:
            rows_data = rows_response.json()
            rows = rows_data.get("items", [])
            print(f"\n✓ Found {len(rows)} rows in {table_name}")

            # Print each row's data with mapped column names
            for i, row in enumerate(rows, 1):
                print(f"\n--- Row {i} (ID: {row.get('id', 'Unknown')}) ---")
                values = row.get("values", {})

                if not values:
                    print("  No values found in this row")
                else:
                    for column_id, cell_data in values.items():
                        # Get the readable column name
                        column_name = column_mapping.get(column_id, column_id)

                        # Try to get readable value
                        display_value = cell_data
                        if isinstance(cell_data, dict):
                            display_value = cell_data.get("displayValue",
                                                        cell_data.get("value",
                                                                    str(cell_data)))

                        # Limit display length for readability
                        if isinstance(display_value, str) and len(display_value) > 100:
                            display_value = display_value[:97] + "..."

                        # Show both the readable name and original ID
                        print(f"  {column_name}: {display_value}")

            inventory_data[table_name] = {
                "rows": rows,
                "columns": column_mapping
            }

        else:
            print(f"✗ {table_name}: Error {rows_response.status_code}")
            print(f"  Response: {rows_response.text}")
            inventory_data[table_name] = {"error": rows_response.status_code}

    return inventory_data

# Test function
if __name__ == "__main__":
    print("Testing direct access to Coda inventory tables...")
    result = get_inventory_data_direct()

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for table_name, data in result.items():
        if isinstance(data, dict) and "rows" in data:
            print(f"  {table_name}: {len(data['rows'])} rows fetched")
            print(f"    Columns mapped: {len(data['columns'])}")
        else:
            print(f"  {table_name}: {data}")