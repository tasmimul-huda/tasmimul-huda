import os
import json
import re
from kaggle.api.kaggle_api_extended import KaggleApi
from urllib.parse import urlparse

# Load from GitHub secrets (environment variables)
USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

if not USERNAME or not KAGGLE_KEY:
    raise ValueError("❌ Kaggle credentials not found in environment variables!")

JSON_FILE = "notebooks.json"
README_FILE = "README.md"

START_TAG = "<!-- KAGGLE_SECTION_START -->"
END_TAG = "<!-- KAGGLE_SECTION_END -->"


def extract_ref_from_url(url: str) -> str:
    """Extract notebook reference (slug) from Kaggle URL."""
    parsed = urlparse(url)
    match = re.search(r"/([^/]+)$", parsed.path)
    return match.group(1) if match else None


def fetch_notebook_by_ref(api, username, ref):
    """Fetch notebook metadata by searching for the ref name."""
    kernels = api.kernels_list(user=username, search=ref, page_size=50)
    for k in kernels:
        if k.ref.split("/")[-1] == ref:
            return {
                "title": k.title,
                "url": f"https://www.kaggle.com/{username}/{ref}",
                "votes": k.total_votes,
            }
    return None


def generate_kaggle_section(notebooks):
    """Generate the markdown section for Kaggle notebooks."""
    lines = [
        # "## 🏆 My Kaggle Notebooks",
        f"[![Kaggle](https://img.shields.io/badge/Kaggle-{USERNAME}-20BEFF?style=flat&logo=kaggle&logoColor=white)](https://www.kaggle.com/{USERNAME})",
        "",
    ]

    if not notebooks:
        lines.append("_No notebooks found or votes below threshold._")
        return "\n".join(lines)

    for nb in notebooks:
        vote = nb["votes"]
        badge = f"![Votes](https://img.shields.io/badge/Votes-{vote}-blue?style=flat&logo=kaggle&logoColor=white)"
        lines.append(f"- 📘 [{nb['title']}]({nb['url']}) {badge}")

    return "\n".join(lines)


def update_readme_section(readme_text, new_section):
    """Replace the section between START_TAG and END_TAG in README."""
    pattern = re.compile(rf"{START_TAG}.*?{END_TAG}", re.DOTALL)
    replacement = f"{START_TAG}\n{new_section}\n{END_TAG}"
    if re.search(pattern, readme_text):
        return re.sub(pattern, replacement, readme_text)
    else:
        # Append if not found
        return f"{readme_text.strip()}\n\n{replacement}\n"


def main():
    print("🚀 Starting Kaggle notebook update...")

    # Initialize Kaggle API (uses ~/.kaggle/kaggle.json created in GitHub Action)
    api = KaggleApi()
    api.authenticate()

    # Load URLs
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)["notebooks"]

    results = []

    for url in urls:
        ref = extract_ref_from_url(url)
        if not ref:
            continue

        nb = fetch_notebook_by_ref(api, USERNAME, ref)
        if nb and nb["votes"] > 10:  # show only those with >10 votes
            results.append(nb)

    # Sort by votes descending
    results.sort(key=lambda x: x["votes"], reverse=True)

    # Create markdown section
    kaggle_section = generate_kaggle_section(results)

    # Read and update README
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_text = f.read()

    updated_text = update_readme_section(readme_text, kaggle_section)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_text)

    print("✅ README.md updated successfully!")


if __name__ == "__main__":
    main()
