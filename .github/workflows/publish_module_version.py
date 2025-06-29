import os
import requests
import json

def create_new_module_version(tfe_hostname, org_name, module_name, provider_name, token, new_version, commit_sha):
    url = f"https://{tfe_hostname}/api/v2/organizations/{org_name}/registry-modules/private/{org_name}/{module_name}/{provider_name}/versions"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/vnd.api+json"}
    data = {
        "data": {
            "type": "registry-module-versions",
            "attributes": {
                "version": new_version,
                "commit-sha": commit_sha
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(f"Version {new_version} created successfully.")
    except requests.RequestException as e:
        print(f"Error creating new version: {e}")

# Read environment variables
tfe_hostname = os.getenv('TFE_HOSTNAME')
org_name = os.getenv('TFE_ORG')
module_name = os.getenv('TFE_MODULE')
provider_name = os.getenv('TFE_PROVIDER')
token = os.getenv('TFE_TOKEN')
commit_sha = os.getenv('COMMIT_SHA')
new_version = os.getenv('NEW_VERSION')

# Ensure all required environment variables are set
if not all([tfe_hostname, org_name, module_name, provider_name, token, commit_sha]):
    print("Error: One or more required environment variables are not set.")
else:
    try:
        create_new_module_version(tfe_hostname, org_name, module_name, provider_name, token, new_version, commit_sha)
    except ValueError as e:
        print(f"Error: {e}")
