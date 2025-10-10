import os
from kaggle.api.kaggle_api_extended import KaggleApi
import re

# Authenticate
api = KaggleApi()
api.authenticate()

# Notebooks to track
notebooks = {
    "eurosat-classification-cnn": "EuroSat Classification CNN",
    "eurosat-classification-with-efficientnet": "EuroSat Classification with EfficientNet",
    "globalwheet-detection-yolov8": "Global Wheat Detection YOLOv8"
}

username = "tasmim"
readme_file = "README.md"

# Fetch votes
votes_badges = {}
for slug, title in notebooks.items():
    kernel = api.kernels_view(username, slug)
    votes = kernel.totalVotes
    badge = f"![Votes](https://img.shields.io/badge/Votes-{votes}-blue?style=flat&logo=kaggle&logoColor=white)"
    votes_badges[title] = badge

# Update README section
with open(readme_file, "r", encoding="utf-8") as f:
    content = f.read()

# Regex to replace previous badges
def replace_badge(match):
    title = match.group(1)
    if title in votes_badges:
        return f"- {match.group(2)} {votes_badges[title]} – {match.group(3)}"
    return match.group(0)

pattern = re.compile(r"- (.+?) \!\[Votes\].+? – (.+)")
content = pattern.sub(lambda m: f"- {m.group(1)} {votes_badges.get(m.group(1), '')} – {m.group(2)}", content)

with open(readme_file, "w", encoding="utf-8") as f:
    f.write(content)

print("README updated with latest Kaggle votes!")
