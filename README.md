# python_cli

Clones repositories locally and runs Snyk CLI against them. 
Works with Github presently.

## REQUIRES

Snyk CLI needs to be installed

## OPTIONAL:

--file - Input your list file for repo names (example list file in repo)

Optionsal ENV
GH_USERNAME - Contains your GH Username
GH_TOKEN - Contains your GH Token
SNYK_TOKEN - Contains your GH Token
SNYK_ORG - Snyk Orgslug ex. https://snyk.io/org/[orgslugname]

## How to use:
- Clone repo
- Navigate into directory
- Run <pre><code>pip install -r requirements.txt</code></pre>
- Run <pre><code>python3 main.py (optional)--file 'listfile.txt' </code></pre>

You will have an output for sca_results_{time}.json, sast_results_{time}.json, and iac_results_{time}.json within your local clone
