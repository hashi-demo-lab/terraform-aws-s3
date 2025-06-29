import os
import requests
import json
from packaging import version

def get_latest_version(tfe_hostname, org_name, module_name, provider_name, token):
    url = f"https://{tfe_hostname}/api/registry/v1/modules/{org_name}/{module_name}/{provider_name}/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        versions = data.get("versions", [])

        if not versions:
            raise ValueError("No versions found")

        sorted_versions = sorted(versions, key=lambda v: version.parse(v), reverse=True)
        latest_version = sorted_versions[0]

        return latest_version
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")

def increment_version(latest_version, release_type):
    major, minor, patch = map(int, latest_version.split('.'))

    if release_type.lower().strip() == "major":
        major += 1
        minor = 0
        patch = 0
    elif release_type.lower().strip() == "minor":
        minor += 1
        patch = 0
    elif release_type.lower().strip() == "patch":
        patch += 1
    else:
        raise ValueError("Invalid release type")

    new_version = f"{major}.{minor}.{patch}"
    return new_version

# Read environment variables
tfe_hostname = os.getenv('TFE_HOSTNAME')
org_name = os.getenv('TFE_ORG')
module_name = os.getenv('TFE_MODULE')
provider_name = os.getenv('TFE_PROVIDER')
token = os.getenv('TFE_TOKEN')
release_type = os.getenv('RELEASE_TYPE')

# Ensure all required environment variables are set
if not all([tfe_hostname, org_name, module_name, provider_name, token]):
    print("Error: One or more required environment variables are not set.")
else:
    latest_version = get_latest_version(tfe_hostname, org_name, module_name, provider_name, token)
    if latest_version:
        #print(f"Latest version: {latest_version}")

        try:
            new_version = increment_version(latest_version, release_type)
            if new_version:
                print(new_version)
        except ValueError as e:
            print(f"Error: {e}")
