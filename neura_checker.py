import shutil
import subprocess
import json
import requests
import sys
from endToEnd import main



# Function to read and parse the requirements.txt file
def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    return [requirement.strip() for requirement in requirements]

    
def install_dependencies(repo_name):
  requirements = parse_requirements(f'{repo_name}/requirements.txt')
  print('requirements:', requirements)
  # Write the filtered dependencies to a new file (e.g., requirements_filtered.txt)
  with open('requirements_filtered.txt', 'w') as file:
    for req in requirements:
      if("tensorflow" not in req):
        file.write(req + '\n')

  print("Filtered dependencies (excluding TensorFlow) have been written to requirements_filtered.txt.")
  subprocess.run(['pip', 'install', '-r', 'requirements_filtered.txt', '--target', '/tmp'])
  

def check_repo(owner, repo_name, token, pr_number):
  sys.path.append('/tmp')
  install_dependencies(repo_name)
  json_config = open(f'{repo_name}/config.json')
  json_config = json.load(json_config)
  shutil.copyfile(src=repo_name+'/'+json_config["fileName"], dst=json_config["fileName"])
  print('Scan Starting...')
  print("Scanning file at path: "+json_config["fileName"]+"...")
  output=main(json_config["fileName"], json_config["inputSize"], json_config["outputSize"], json_config["parserName"], json_config["resultFileName"])
  print('Scan completed.')
  print('Writing results as a GitHub comment...')
  write_output_as_github_comment(owner, repo_name, token, output, pr_number)
  print('GitHub comment done.')

    
def write_output_as_github_comment(owner, repo_name, token, data, pr_number):
   headers = {'Authorization': f'Bearer {token}', 'X-GitHub-Api-Version':'2022-11-28', 'Accept':'application/vnd.github+json'}
   comment_github_url=f'https://api.github.com/repos/{owner}/{repo_name}/issues/{pr_number}/comments'
   print('url: ', comment_github_url)
   data=json.dumps({"body":data})
   result=requests.post(comment_github_url, headers=headers, data=data)
