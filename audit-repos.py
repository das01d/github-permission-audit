import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
org = "sherwin-williams-co"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Get list of repos that have the correct topic
search_url = f"https://api.github.com/search/repositories?q=topic:business-platforms+org:{org}&per_page=100"
repos = requests.get(search_url, headers=headers).json().get('items', [])
ds_list_of_repos_from_topic = pd.DataFrame(repos).loc[:,'name']

# Get list of repos from our groups that should have access
def get_team_repos(team_slug):
    repos_url = f"https://api.github.com/orgs/{org}/teams/{team_slug}/repos?per_page=100"
    response = requests.get(repos_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise(f"Error: {response.status_code}") 

resp_admins = get_team_repos(team_slug = "gg-aad-dss-digitalit-iom-gatekeepers")
resp_devs = get_team_repos(team_slug = "gg-aad-dss-digitalit-iom-developers")

def shape_data(resp):
    temp_data_frame = pd.DataFrame(resp)

    # extract the permissions.admin attribute from the json in the 'permissions' column
    temp_data_frame['has_admin_permission'] = temp_data_frame['permissions'].apply(lambda x: x['admin'])

    # reshape to only include the rows needed
    temp_data_frame = pd.DataFrame(temp_data_frame.loc[:,['name','has_admin_permission', 'topics']])
    return temp_data_frame

ds_admin_repos = shape_data(resp_admins)
ds_dev_repos = shape_data(resp_devs)

# Get a unique list of all the repos
ds_all_repos = pd.concat([ds_admin_repos, ds_dev_repos, ds_list_of_repos_from_topic], axis=0)

# keep only the name and topics column
ds_all_repos = pd.DataFrame(ds_all_repos.loc[:,['name', 'topics']])

# remove duplicates
ds_all_repos = ds_all_repos.drop_duplicates(subset='name').reset_index(drop=True)

# Copy all_repos into a new "report" dataframe
ds_report = ds_all_repos.copy()

## Report on the topic being present
ds_report['topic-present'] = False
for r in ds_list_of_repos_from_topic:
    ds_report.loc[ds_report['name'] == r, 'topic-present'] = True

# loop through ds_admin_repos.  update the column 'has-admin-team-present' to true in the ds_report data frame where the repo name matches
for r in ds_dev_repos['name' ]:
    # lookup name ds_report name column and update 'dev-team-present' to true if it exists
    ds_report.loc[ds_report['name'] == r, 'dev-team-present'] = True
    # update 'dev-team-has-admin-permission' to true if the repo has admin permission
    # set the value to the opposite of values[0], assuming it is boolean
    ds_report.loc[ds_report['name'] == r, 'dev-team-does-not-have-admin-permission'] = not ds_dev_repos.loc[ds_dev_repos['name'] == r, 'has_admin_permission'].values[0]
    
for r in ds_admin_repos['name' ]:
    # lookup name ds_report name column and update 'dev-team-present' to true if it exists
    ds_report.loc[ds_report['name'] == r, 'gatekeeper-team-present'] = True
    # update 'dev-team-has-admin-permission' to true if the repo has admin permission
    ds_report.loc[ds_report['name'] == r, 'gatekeeper-team-has-admin-permission'] = ds_admin_repos.loc[ds_admin_repos['name'] == r, 'has_admin_permission'].values[0]

ds_report.to_csv(f"report-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv", index=False)