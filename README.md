# GitHub Repo Sync Tool

This tool is designed to help you automatically clone or pull all repositories from your GitHub account. It's especially handy if you switch between multiple machines and want to keep your codebase up-to-date on all of them.
## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/PapaPeskwo/repo-sync
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up the .env file:

Copy the sample configuration from .env.example (if you have one) or create a new .env file in the root directory with the following structure:

```dotenv
GITHUB_USERNAME=YOUR_GITHUB_USERNAME
GITHUB_TOKEN=YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
BASE_DIR=/path/to/your/projects/directory
SKIP_REPOS=RepoNameToSkip1,RepoNameToSkip2
```

## Token Permissions

When generating a Personal Access Token (PAT) from GitHub for this tool, ensure it has the following permissions:

- repo: This grants full control of private repositories, which includes:
    - repo:status - Access commit status.
    - repo_deployment - Access deployment status.
    - public_repo - Access public repositories.
    - repo:invite - Access repository invitations.
    - security_events - Read security vulnerability alerts.
- read:user: Grants access to read a user’s profile data.

To create a token:

1. Navigate to your GitHub settings.
2. Under "Developer settings", click on "Personal access tokens".
3. Click "Generate new token".
4. Provide a descriptive name for the token.
5. Select the required permissions.
6. Generate the token and save it securely. Once you navigate away, you won't be able to see the token again.

## Usage

Once you've set up the .env file and installed the requirements:

```bash
python repo_sync.py
```

This will either clone new repositories or pull the latest changes for existing repositories from your GitHub account, based on the configurations in the .env file.
Security

## Contributing

Contributions are welcome! Please create an issue or open a pull request with your changes.