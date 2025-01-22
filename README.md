# Github Permissions Audit - Business Platforms

## About <a name = "about"></a>

The scripts in this repo are to help with the following:

* Gather the teams repos and ensure they are meeting our standards for topics and team permissions.
* Update repo custom properties to reflect the association to the CMDB.

### Prerequisites

#### Add .env file with GITHUB_TOKEN for your API Token

You should generate an API key with the following permissions:

```
repo
admin:org.read:org
user.read:user
```

Once generated, you must grant access the the SW org by using the **Configure SSO**.  This is in the list of API keys, just next to the API key that you generate.

#### Install requirements

```cmd
pip install -r ./requirements.txt
```
## Usage <a name = "usage"></a>

### Audit repo against standards

Execute script and evaluate ./reports/report-{timestamp}.csv.

```cmd
python ./audit-repos.py
```

### Update repo CMDB Custom Properties

Create an excel file that maps repo names to the CMDB Business Appliation and Services.  Run the update-repos-cmdb-custom-props.py to apply the changes.

Update SPREADSHEET_FILE and WORKSHEET_NAME to reflect your mapping spreadsheet.  

Your spreadsheet should have the following columns:

* Repo
* Business App
* Service

```cmd
python ./update-repos-cmdb-custom-props.py
```