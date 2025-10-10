import os
import re
from kaggle.api.kaggle_api_extended import KaggleApi

# Authenticate Kaggle API
api = KaggleApi()
api.authenticate()

# Notebooks with frameworks used
notebooks = [
    {
        "slug": "neuralps-xtra-data-augment-multimodels",
        "title": "NeuralPS Xtra Data Augment MultiModels",
        "emoji": "🧠",
        "frameworks": ["Python", "PyTorch", "Scikit-learn"]
    },
    {
        "slug": "eurosat-classification-cnn",
        "title": "EuroSat Classification CNN",
        "emoji": "🖼️",
        "frameworks": ["Python", "TensorFlow", "Keras"]
    },
    {
        "slug": "rsna-training-efficientnet",
        "title": "RSNA Training EfficientNet",
        "emoji": "🤖",
        "frameworks": ["Python", "TensorFlow", "Keras"]
    },
    {
        "slug": "rules-classifier-xgb-lr-lgbm-cat",
        "title": "Rules Classifier XGB/LR/LGBM/CAT",
        "emoji": "📊",
        "frameworks": ["Python", "Scikit-learn", "XGBoost", "LightGBM", "CatBoost"]
    }
]

username = "tasmim"
readme_file = "README.md"

# Helper: generate framework badges
def generate_framework_badges(frameworks):
    badge_template = "![{name}](https://img.shields.io/badge/{name}-{color}?style=flat&logo={logo}&logoColor=white)"
    logos = {
        "Python": ("Python", "3776AB"),
        "PyTorch": ("pytorch", "EE4C2C"),
        "TensorFlow": ("tensorflow", "FF6F00"),
        "Keras": ("keras", "D00000"),
        "Scikit-learn": ("scikit-learn", "F7931E"),
        "XGBoost": ("xgboost", "0E8A16"),
        "LightGBM": ("lightgbm", "00AABB"),
        "CatBoost": ("catboost", "FF6600")
    }
    badges = []
    for fw in frameworks:
        logo, color = logos.get(fw, (fw, "4B4B4B"))
        badges.append(badge_template.format(name=fw, color=color, logo=logo))
    return " ".join(badges)

# Generate notebook lines
updated_lines = []
for nb in notebooks:
    try:
        kernel = api.kernels_view(username, nb["slug"], "code")
        votes = kernel.totalVotes
        url = f"https://www.kaggle.com/code/{username}/{nb['slug']}"
        votes_badge = f"![Votes](https://img.shields.io/badge/Votes-{votes}-blue?style=flat&logo=kaggle&logoColor=white)"
        framework_badges = generate_framework_badges(nb["frameworks"])
        line = f"- {nb['emoji']} [{nb['title']}]({url}) {framework_badges} {votes_badge}"
        updated_lines.append(line)
    except Exception as e:
        print(f"Failed to fetch {nb['title']}: {e}")

# Read current README
with open(readme_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Kaggle section
pattern = re.compile(r"(### 🏆 Kaggle Notebooks\n)(.*?)(\n### |\Z)", re.DOTALL)
new_section = "### 🏆 Kaggle Notebooks\n" + "\n".join(updated_lines) + "\n\n"
content = pattern.sub(lambda m: new_section + m.group(3), content)

# Write updated README
with open(readme_file, "w", encoding="utf-8") as f:
    f.write(content)

print("README updated successfully with latest Kaggle votes and framework badges!")
