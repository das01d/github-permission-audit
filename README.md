# Github Permissions Audit - Business Platforms

## Table of Contents

- [About](#about)
- [Usage](#usage)

## About <a name = "about"></a>

Gather the teams repos and ensure they are meeting our standards for topics and team permissions.

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

Execute script and evaluate report.csv.

```cmd
python ./audit-repos.py
```
