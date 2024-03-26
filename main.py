import os
import subprocess
import argparse
import time
from datetime import datetime
from git import Repo

parser = argparse.ArgumentParser(description='file: input the file path to your repo list file')
parser.add_argument("--file")
args = parser.parse_args()
repo_file = args.file
start_dir = os.getcwd()

if "GH_USERNAME" in os.environ:
    username = os.environ['GH_USERNAME']
else:
    print("Enter your GH User")
    username = input()
if "GH_TOKEN" in os.environ:
    gh_token = os.environ['GH_TOKEN']
else:
    print("Enter your GH Token")
    gh_token = input()
if "SNYK_TOKEN" in os.environ:
    snyk_token = os.environ['SNYK_TOKEN']
else:
    print("Enter your Snyk API Token")
    snyk_token = input()
if not repo_file:
    print("Enter the repo list file")
    repo_file = input()
if "SNYK_ORG" in os.environ:
    snyk_org = os.environ['SNYK_ORG']
else:
    print("Enter the your Snyk org slug 'https://snyk.io/org/[orgslugname]'")
    snyk_org = input()

with open(repo_file, 'r') as file:
    paths = file.read().splitlines()

for r in paths:
    if os.path.exists(os.path.join(os.getcwd(), f'{r}')):
        print(f'{r} already cloned')
    else:
        Repo.clone_from(f"https://{username}:{gh_token}@github.com/{r}.git", f"{r}")

for r in paths:
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d.%H%M")
    if os.name == 'nt':
        os.chdir(f'./{r}')
        os.system(f'snyk-win.exe auth {snyk_token}')
        subprocess.run(f'snyk-win.exe test --org={snyk_org} --all-projects --fail-fast --json-file-output=sca_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk-win.exe code test --org={snyk_org} --json-file-output=sast_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk-win.exe iac test --org={snyk_org} --json-file-output=iac_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk-win.exe sbom --org={snyk_org} --all-projects --format=cyclonedx1.5+json --json-file-output=sbom_{timestamp}.json', check=False)
        os.chdir(f'{start_dir}')
        time.sleep(5)
    else:
        os.chdir(f'./{r}')
        os.system(f'snyk auth {snyk_token}')
        subprocess.run(f'snyk test --org={snyk_org} --all-projects --fail-fast --json-file-output=sca_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk code test --org={snyk_org} --json-file-output=sast_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk iac test --org={snyk_org} --json-file-output=iac_results_{timestamp}.json', check=False)
        subprocess.run(f'snyk sbom --org={snyk_org} --all-projects --format=cyclonedx1.5+json --json-file-output=sbom_{timestamp}.json', check=False)
        os.chdir(f'{start_dir}')
        time.sleep(5)
