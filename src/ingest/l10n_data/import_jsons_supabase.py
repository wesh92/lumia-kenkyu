import json
from supabase import create_client, Client
import tomllib

with open('.secrets.toml', "rb") as f:
    secrets = tomllib.load(f)
    SUPABASE_URL = secrets['supabase']['url']
    SUPABASE_KEY = secrets['supabase']['key']
# Supabase setup
url: str = SUPABASE_URL
key: str = SUPABASE_KEY
supabase: Client = create_client(url, key)

def import_item_names(json_file_path: str, column_1_name: str, column_2_name: str):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        import_data: dict = json.load(file)

    # Prepare the data for insertion
    # Data keys can be arbitrary so we dynamically create a list of dictionaries
    items_to_insert = [{column_1_name: key, column_2_name: value} for key, value in import_data.items()]

    # Split the data into chunks of 1000 items each
    chunk_size = 1000
    for i in range(0, len(items_to_insert), chunk_size):
        chunk = items_to_insert[i:i+chunk_size]

        # Insert the chunk into Supabase
        data, count = supabase.table("item_names").insert(chunk).execute()

        print(f"Inserted {len(chunk)} items. Total inserted: {i + len(chunk)}")

    print("Data import completed.")

if __name__ == "__main__":
    import_item_names('jsons/item_name.json', "item_id", "item_name")
