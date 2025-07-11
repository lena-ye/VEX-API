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
# Option 2 - Recursively resolve all $ref entries
# ==========

def resolve_refs(obj, schemas, preserve_ref=True):
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref_path = obj["$ref"]
            if ref_path.startswith("#/components/schemas/"):
                schema_name = ref_path.split("/")[-1]
                ref_schema = schemas.get(schema_name, {})
                resolved = resolve_refs(ref_schema, schemas, preserve_ref=True)
                if preserve_ref:
                    return {
                        "_originalRef": ref_path,
                        **resolved
                    }
                else:
                    return resolved
        return {k: resolve_refs(v, schemas, preserve_ref=preserve_ref) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_refs(item, schemas, preserve_ref=preserve_ref) for item in obj]
    else:
        return obj

# Ask for schema name to expand
schema_name = "Skill" # MODIFY THIS PART

if schema_name not in schemas:
    print(f"Schema '{schema_name}' not found.")
    exit(1)

expanded = resolve_refs(schemas[schema_name], schemas, preserve_ref=True)

# Save expanded schema to JSON
json_path = os.path.join(script_dir, f"{schema_name}_expanded.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({schema_name: expanded}, f, indent=2)

print(f"{schema_name} schema saved to {schema_name}_expanded.json")

# ==========
# End of Option 2
# ==========
