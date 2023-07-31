import jwt
import time
import requests
import os
import neura_checker
import json


pem = "neuralintchecker.private-key.pem"
# Get the App ID
app_id=369366
# Open PEM
with open(pem, 'rb') as pem_file:
    private_key = pem_file.read()

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': app_id,
}
encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

def handler(event, context):
  data=json.loads(event['body'])
  if data['action']=='opened':
     owner=data['pull_request']['head']['repo']['owner']['login']
     repo_name=data['pull_request']['head']['repo']['name']
     branch_name=data['pull_request']['base']['ref']
     pr_number=data['number']
  token=clone_repo(owner, repo_name, branch_name)
  neura_checker.check_repo(owner, repo_name, token, pr_number)
  return "return"


# Repo full name is owner_name/repo_name
def clone_repo(owner, repo_name, branch_name):
  # Get the installation ID
  url_to_get_installation_id=f'https://api.github.com/repos/{owner}/{repo_name}/installation'
  headers = {'Authorization': f'Bearer {encoded_jwt}', 'X-GitHub-Api-Version':'2022-11-28', 'Accept':'application/vnd.github+json'}
  response = requests.get(url_to_get_installation_id, headers=headers)
  installation_id = response.json()['id']
  # get the token
  url_to_get_token = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
  response = requests.post(url_to_get_token, headers=headers)
  token = response.json()['token']
  print('token: '+token)
  # Construct the API URL for cloning the repository
  clone_url = f"https://x-access-token:{token}@github.com/{owner}/{repo_name}.git"
  # Use the clone URL to clone the repository with Git
  os.chdir('/tmp')
  os.system(f"git clone -b {branch_name} {clone_url}")
  return token
