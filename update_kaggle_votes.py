import os
import re
from kaggle.api.kaggle_api_extended import KaggleApi

# Authenticate Kaggle API
api = KaggleApi()
api.authenticate()

# Notebooks to track
notebooks = [
    {
        "slug": "neuralps-xtra-data-augment-multimodels",
        "title": "NeuralPS Xtra Data Augment MultiModels",
        "emoji": "🧠",
        "badge": "![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)"
    },
    {
        "slug": "eurosat-classification-cnn",
        "title": "EuroSat Classification CNN",
        "emoji": "🖼️",
        "badge": "![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)"
    },
    {
        "slug": "rsna-training-efficientnet",
        "title": "RSNA Training EfficientNet",
        "emoji": "🤖",
        "badge": "![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)"
    },
    {
        "slug": "rules-classifier-xgb-lr-lgbm-cat",
        "title": "Rules Classifier XGB/LR/LGBM/CAT",
        "emoji": "📊",
        "badge": "![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)"
    }
]

username = "tasmim"
readme_file = "README.md"

# Prepare updated notebook lines
updated_lines = []

for nb in notebooks:
    try:
        kernel = api.kernels_view(username, nb["slug"], "code")  # Important: "code" type
        votes = kernel.totalVotes
        url = f"https://www.kaggle.com/code/{username}/{nb['slug']}"
        votes_badge = f"![Votes](https://img.shields.io/badge/Votes-{votes}-blue?style=flat&logo=kaggle&logoColor=white)"
        line = f"- {nb['emoji']} [{nb['title']}]({url}) {nb['badge']} {votes_badge}"
        updated_lines.append(line)
    except Exception as e:
        print(f"Failed to fetch {nb['title']}: {e}")

# Read current README
with open(readme_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Kaggle section
# It assumes your README section starts with "### 🏆 Kaggle Notebooks" and ends before the next H3
pattern = re.compile(r"(### 🏆 Kaggle Notebooks\n)(.*?)(\n### |\Z)", re.DOTALL)
new_section = "### 🏆 Kaggle Notebooks\n" + "\n".join(updated_lines) + "\n\n"
content = pattern.sub(lambda m: new_section + m.group(3), content)

# Write updated README
with open(readme_file, "w", encoding="utf-8") as f:
    f.write(content)

print("README updated successfully with latest Kaggle votes and links!")
