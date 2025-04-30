import os
import requests
import re

username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

# fetch repos
url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
response = requests.get(url, headers={"Authorization": f"token {token}"})
repos = response.json()

# filter out private repos and forks
filtered_repos = [
    repo for repo in repos if not repo["private"] and not repo["fork"]
]

# build html
generated_html = ['<h3>Projects</h3>', '<p>', '<ul>']
for repo in filtered_repos:
    name = repo["name"]
    url = repo["html_url"]
    desc = repo["description"] or "No description."
    generated_html.append(f'<li><a href="{url}">{name}</a> - {desc}</li>')
generated_html.append('</ul>')
generated_html.append('</p>')

generated_html_str = "\n".join(generated_html)

# load projects.html
with open("projects.html", "r") as f:
    content = f.read()

# replace content between comment markers
new_content = re.sub(
    r'<!-- START GENERATED PROJECTS -->.*?<!-- END GENERATED PROJECTS -->',
    f'<!-- START GENERATED PROJECTS -->\n{generated_html_str}\n<!-- END GENERATED PROJECTS -->',
    content,
    flags=re.DOTALL
)

# save updated html
with open("projects.html", "w") as f:
    f.write(new_content)