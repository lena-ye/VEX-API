import requests
import yaml
import json
import os

# Get the directory of this Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Download swagger.yml
url = "https://www.robotevents.com/api/v2/swagger.yml"
response = requests.get(url)

if response.status_code == 200:
    yaml_path = os.path.join(script_dir, "swagger.yml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Downloaded swagger.yml successfully.")
else:
    print(f"Failed to download swagger.yml: {response.status_code}")
    exit(1)

# Load and parse the swagger.yml
with open(yaml_path, "r", encoding="utf-8") as f:
    spec = yaml.safe_load(f)

schemas = spec.get("components", {}).get("schemas", {})

# ==========
# Option 1 - Access one specific schema (now user-defined)
# ==========

schema_name = "Skill" # MODIFY THIS PART

schema_obj = schemas.get(schema_name)
if schema_obj:
    output_path = os.path.join(script_dir, f"{schema_name}_skeleton.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({schema_name: schema_obj}, f, indent=2)
    print(f"Saved {schema_name} schema.")
else:
    print(f"Schema '{schema_name}' not found.")

# ==========
# End of Option 1 
# ==========
