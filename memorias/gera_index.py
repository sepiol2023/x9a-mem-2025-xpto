import os
import json
from datetime import datetime, timezone

# Config fixo
GITHUB_USER = "sepiol2023"
REPO_NAME = "x9a-mem-2025-xpto"
BRANCH = "main"

# Base URL RAW do GitHub
BASE_RAW = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/"

# Pasta raiz local do projeto (onde o script está)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Lista de arquivos
files_list = []
for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file == "index.json":  # Ignora o próprio index
            continue
        local_path = os.path.relpath(os.path.join(root, file), ROOT_DIR).replace("\\", "/")
        files_list.append({
            "path": local_path,
            "url": BASE_RAW + local_path
        })

# Monta estrutura JSON
payload = {
    "version": 1,
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "github": {
        "user": GITHUB_USER,
        "repo": REPO_NAME,
        "branch": BRANCH
    },
    "base_raw": BASE_RAW,
    "count": len(files_list),
    "files": files_list
}

# Salva arquivo index.json
with open(os.path.join(ROOT_DIR, "index.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print(f"[ok] index.json gerado com {len(files_list)} arquivos.")
