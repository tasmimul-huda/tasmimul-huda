# File: .github/workflows/update_kaggle_votes.py

import os
import requests

# ------------------------------
# CONFIG
# ------------------------------
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")
README_FILE = "README.md"
START_MARKER = "<!-- BEGIN KAGGLE NOTEBOOKS -->"
END_MARKER = "<!-- END KAGGLE NOTEBOOKS -->"

# Map your frameworks/libraries keywords to badges
FRAMEWORK_BADGES = {
    "python": "![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)",
    "tensorflow": "![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)",
    "keras": "![Keras](https://img.shields.io/badge/Keras-D00000?style=flat&logo=keras&logoColor=white)",
    "pytorch": "![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)",
    "scikit": "![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)",
    "xgboost": "![XGBoost](https://img.shields.io/badge/XGBoost-0E8A16?style=flat&logo=xgboost&logoColor=white)",
    "lightgbm": "![LightGBM](https://img.shields.io/badge/LightGBM-00AABB?style=flat&logo=lightgbm&logoColor=white)",
    "catboost": "![CatBoost](https://img.shields.io/badge/CatBoost-FF6600?style=flat&logo=catboost&logoColor=white)"
}

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
def fetch_kaggle_notebooks(username):
    """
    Fetch notebooks from Kaggle using the public API
    Returns list of dict: [{'title':..., 'url':..., 'votes':..., 'tags':...}]
    """
    url = f"https://www.kaggle.com/api/v1/users/{username}/kernels"
    try:
        response = requests.get(url, auth=(KAGGLE_USERNAME, KAGGLE_KEY))
        response.raise_for_status()
        data = response.json()
        notebooks = []
        for nb in data:
            notebooks.append({
                "title": nb.get("title"),
                "url": f"https://www.kaggle.com/{username}/{nb.get('ref')}",
                "votes": nb.get("totalVotes", 0),
                "tags": [t.lower() for t in nb.get("language", [])] if nb.get("language") else []
            })
        return notebooks
    except Exception as e:
        print(f"Error fetching Kaggle notebooks: {e}")
        return []

def get_badges(tags):
    """Return badges based on notebook tags"""
    badges = []
    for tag in tags:
        for key in FRAMEWORK_BADGES:
            if key in tag:
                badges.append(FRAMEWORK_BADGES[key])
    if "python" not in tags:
        badges.insert(0, FRAMEWORK_BADGES["python"])  # always include Python badge
    return " ".join(badges)

def generate_notebook_lines(notebooks):
    """Generate markdown lines for README"""
    lines = []
    for nb in notebooks:
        badges = get_badges(nb["tags"])
        votes = f"![Votes](https://img.shields.io/badge/Votes-{nb['votes']}-blue?style=flat&logo=kaggle&logoColor=white)"
        line = f"- [{nb['title']}]({nb['url']}) {badges} {votes}"
        lines.append(line)
    return lines

def update_readme(lines):
    """Update README.md between markers"""
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        if START_MARKER not in content or END_MARKER not in content:
            print("Markers not found in README, skipping update.")
            return
        before = content.split(START_MARKER)[0] + START_MARKER + "\n"
        after = "\n" + END_MARKER + content.split(END_MARKER)[1]
        new_content = before + "\n".join(lines) + after
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error updating README.md: {e}")

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    notebooks = fetch_kaggle_notebooks(KAGGLE_USERNAME)
    if not notebooks:
        print("No notebooks found or failed to fetch. Exiting without changing README.")
    else:
        md_lines = generate_notebook_lines(notebooks)
        update_readme(md_lines)
