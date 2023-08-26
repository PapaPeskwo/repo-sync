import requests
import os
import subprocess
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
BASE_DIR = os.getenv('BASE_DIR')
SKIP_REPOS = os.getenv('SKIP_REPOS').split(',')

log_messages = []

def log(message):
    print(message)
    log_messages.append(message)

def get_all_user_repositories():
    page = 1
    repos = []
    while True:
        response = requests.get(f'https://api.github.com/user/repos?page={page}&per_page=100',
                                headers={'Authorization': f'token {GITHUB_TOKEN}'})
        
        response_data = response.json()
        if not response_data:
            break
        repos.extend(response_data)
        page += 1
    return repos

def filter_repositories(repos, repo_type):
    if repo_type == 'private':
        return [repo for repo in repos if repo['private']]
    elif repo_type == 'public':
        return [repo for repo in repos if not repo['private']]
    else:
        return repos

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        choice = input(f"Directory {directory} does not exist. Would you like to create it (1) or exit (2)? ")
        if choice == "1":
            os.makedirs(directory)
        elif choice == "2":
            exit("Exiting the program. Please set the correct BASE_DIR in the .env file.")
        else:
            print("Invalid choice. Exiting.")
            exit(1)

def main():
    # Ensure BASE_DIR exists or ask user to create it
    ensure_directory_exists(BASE_DIR)

    # Ask the user for repository type
    while True:
        repo_type = input("Which repositories do you want to pull? (private/public/all): ").lower()
        if repo_type in ['private', 'public', 'all']:
            break
        print("Invalid choice. Please select 'private', 'public', or 'all'.")

    repos = get_all_user_repositories()
    repos = filter_repositories(repos, repo_type)

    for repo in repos:
        repo_name = repo['name']
        repo_clone_url = repo['clone_url']

        if repo_name in SKIP_REPOS:
            log(f"Skipping {repo_name}...")
            continue

        repo_path = os.path.join(BASE_DIR, repo_name)
        if os.path.exists(repo_path):
            log(f"Pulling latest for {repo_name}...")
            subprocess.run(['git', 'pull'], cwd=repo_path)
        else:
            log(f"Cloning {repo_name}...")
            subprocess.run(['git', 'clone', repo_clone_url], cwd=BASE_DIR)

    choice = input("\nOperations complete. Would you like to generate a log file (1) or exit (2)? ")
    if choice == "1":
        log_file_path = os.path.join(BASE_DIR, "operation_log.txt")
        with open(log_file_path, 'w') as log_file:
            for message in log_messages:
                log_file.write(message + '\n')
        print(f"Log file saved to {log_file_path}")
    elif choice != "2":
        print("Invalid choice. Exiting without saving log.")
    input("Press enter to exit.")

if __name__ == "__main__":
    main()
