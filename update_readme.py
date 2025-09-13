import requests
import os
from datetime import datetime

def fetch_repositories():
    username = "AutobahnAuffahrt"
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    response.raise_for_status()
    repos = response.json()

    own_repos = []
    forked_repos = []

    for repo in repos:
        repo_data = {
            "name": repo["name"],
            "html_url": repo["html_url"],
            "updated_at": repo["updated_at"][:10],
        }
        if repo["fork"]:
            forked_repos.append(repo_data)
        else:
            own_repos.append(repo_data)

    return own_repos, forked_repos

def generate_markdown_table(repos):
    table = "| Name | Last Updated | Link |\n|------|--------------|------|\n"
    for repo in repos:
        table += f"| {repo['name']} | {repo['updated_at']} | [Link]({repo['html_url']}) |\n"
    return table

def update_readme(own_repos, forked_repos):
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    start_marker = "<!-- START REPO LIST -->"
    end_marker = "<!-- END REPO LIST -->"

    start_index = next((i for i, line in enumerate(content) if start_marker in line), None)
    end_index = next((i for i, line in enumerate(content) if end_marker in line), None)

    if start_index is None or end_index is None:
        raise ValueError("Markers for repository list not found in README.md")

    updated_content = content[:start_index + 1]
    updated_content.append("\n## My Repositories\n")
    updated_content.append(generate_markdown_table(own_repos))
    updated_content.append("\n## Forked Repositories\n")
    updated_content.append(generate_markdown_table(forked_repos))
    updated_content.append("\n")
    updated_content.extend(content[end_index:])

    with open(readme_path, "w", encoding="utf-8") as file:
        file.writelines(updated_content)

def main():
    own_repos, forked_repos = fetch_repositories()
    update_readme(own_repos, forked_repos)

if __name__ == "__main__":
    main()