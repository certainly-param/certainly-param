"""
Test script to verify the stats calculation logic
Run this locally to test before pushing the workflow
"""
import os
import requests

# You'll need to set your GitHub token as an environment variable
# Or replace this with your token (for testing only - don't commit tokens!)
token = os.environ.get('GITHUB_TOKEN') or input("Enter your GitHub token (or set GITHUB_TOKEN env var): ").strip()
username = 'certainly-param'

if not token:
    print("Error: GitHub token is required")
    exit(1)

# Fetch all repositories
print(f"Fetching all repositories for {username}...")
total_stars = 0
total_forks = 0
page = 1
per_page = 100

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

while True:
    url = f'https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}&type=all'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos = response.json()
    
    if not repos:
        break
    
    for repo in repos:
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        total_stars += stars
        total_forks += forks
        print(f"  {repo['name']}: {stars} stars, {forks} forks")
    
    print(f"Page {page}: Processed {len(repos)} repos. Running totals - Stars: {total_stars}, Forks: {total_forks}")
    
    if len(repos) < per_page:
        break
    
    page += 1

print(f"\n{'='*50}")
print(f"Final totals:")
print(f"  Total Stars: {total_stars}")
print(f"  Total Forks: {total_forks}")
print(f"{'='*50}")

# Show what the badges will look like
stars_badge = f"![GitHub Stars](https://img.shields.io/badge/STARS-{total_stars}-00ff00?style=flat-square&labelColor=0d1117)"
forks_badge = f"![GitHub Forks](https://img.shields.io/badge/FORKS-{total_forks}-00ff00?style=flat-square&labelColor=0d1117)"

print(f"\nBadge URLs:")
print(f"  {stars_badge}")
print(f"  {forks_badge}")
