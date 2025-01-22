import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

SPREADSHEET_FILE = './reports/CMDB Config - Final - 2025-01-21.xlsx'
WORKSHEET_NAME = 'Map'

ORG = "sherwin-williams-co"

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# get custom property of the repo
# only properties with values set are returned
def get_repo_custom_property(repo_name):
    url = f"https://api.github.com/repos/{ORG}/{repo_name}/properties/values"
    response = requests.get(url, headers=headers)
    response_json = response.json()

    #initialize props
    props = {}

    for prop in response_json:
        props =  {prop["property_name"]: prop["value"]}

    return props

def update_repo_custom_property(repo_name, custom_property_name, custom_property_value):
    url = f"https://api.github.com/repos/{ORG}/{repo_name}/properties/values"
    json = {
        "properties": [
            {
                "property_name": custom_property_name,
                "value": custom_property_value
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=json)
    return response.status_code

# Loop through a spreadsheet with the mappings and update the custom properties to align with the CMDB
mapping = pd.read_excel(SPREADSHEET_FILE, sheet_name=WORKSHEET_NAME)

errors_with_business_app_updates = {}
errors_with_service_updates = {}

for index, row in mapping.iterrows():
    repo_name = row['Repo']

    business_app_property_name = "CMDB-Business-Application-Number"
    business_app_value = row['Business App']

    service_property_name = "CMDB-Business-Service-Number"
    service_value = row['Service']

    # update the custom properties
    status_code = update_repo_custom_property(repo_name, custom_property_name=business_app_property_name, custom_property_value=business_app_value)
    print(f"Updated {repo_name} custom value {business_app_property_name} with value {business_app_value} status code {status_code}")

    if status_code != 204:
        errors_with_business_app_updates[repo_name] = {status_code: status_code}

    status_code = update_repo_custom_property(repo_name, custom_property_name=service_property_name, custom_property_value=service_value)
    print(f"Updated {repo_name} custom value {service_property_name} with value {service_value} status code {status_code}")

    if status_code != 204:
        errors_with_service_updates[repo_name] = {'status_code': status_code}

print("business app errors")
print(errors_with_business_app_updates)

print("service errors")
print(errors_with_service_updates)