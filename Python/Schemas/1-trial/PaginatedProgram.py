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

'''
# ==========
# Option 1 - Access one specific schema
# ==========

paginated_program = schemas.get("PaginatedProgram")
if paginated_program:
    paginated_path = os.path.join(script_dir, "PaginatedProgram_skeleton.json")
    with open(paginated_path, "w", encoding="utf-8") as f:
        json.dump({"PaginatedProgram": paginated_program}, f, indent=2)
    print("Saved PaginatedProgram schema.")
else:
    print("PaginatedProgram schema not found.")


# ==========
# End of Option 1 
# ==========

'''

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
        return {k: resolve_refs(v, schemas) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_refs(item, schemas) for item in obj]
    else:
        return obj

# Expand the PaginatedProgram schema
paginated_program = schemas.get("PaginatedProgram", {})
expanded = resolve_refs(paginated_program, schemas)

# Save expanded schema to JSON
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(__file__))[0] + ".json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"PaginatedProgram": expanded}, f, indent=2)

print(f"PaginatedProgram schema saved to {json_path}")

# ==========
# End of Option 2
# ==========
