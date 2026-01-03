import os
import subprocess
import requests

def get_github_access_token():
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    if repl_identity:
        x_replit_token = f'repl {repl_identity}'
    elif web_repl_renewal:
        x_replit_token = f'depl {web_repl_renewal}'
    else:
        raise Exception('X_REPLIT_TOKEN not found')
    
    response = requests.get(
        f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github',
        headers={
            'Accept': 'application/json',
            'X_REPLIT_TOKEN': x_replit_token
        }
    )
    
    data = response.json()
    connection = data.get('items', [{}])[0]
    settings = connection.get('settings', {})
    
    access_token = settings.get('access_token') or settings.get('oauth', {}).get('credentials', {}).get('access_token')
    
    if not access_token:
        raise Exception('GitHub not connected or no access token found')
    
    return access_token

def get_github_username(token):
    response = requests.get(
        'https://api.github.com/user',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    return response.json().get('login')

def create_repo(token, repo_name):
    response = requests.post(
        'https://api.github.com/user/repos',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            'name': repo_name,
            'description': 'Lottery Prediction Platform - Euromillions & French Loto',
            'private': False
        }
    )
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully!")
        return response.json()
    elif response.status_code == 422:
        print(f"Repository '{repo_name}' already exists, will use existing repo")
        return {'already_exists': True}
    else:
        print(f"Error creating repo: {response.status_code} - {response.text}")
        return None

if __name__ == '__main__':
    token = get_github_access_token()
    username = get_github_username(token)
    print(f"Connected as GitHub user: {username}")
    
    repo_name = "lottery-prediction-platform"
    result = create_repo(token, repo_name)
    
    if result:
        remote_url = f"https://{token}@github.com/{username}/{repo_name}.git"
        print(f"\nRepository URL: https://github.com/{username}/{repo_name}")
        print(f"\nTo push your code, run these commands in the Shell:")
        print(f"  git remote add origin https://github.com/{username}/{repo_name}.git")
        print(f"  git push -u origin main")
