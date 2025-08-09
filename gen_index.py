# scripts/gen_index.py
import os, json, mimetypes
from datetime import datetime, timezone

# === CONFIG HARDcoded (com fallback para env) ===
GITHUB_USER  = os.getenv("INDEX_GH_USER",  "sepiol2023")
REPO_NAME    = os.getenv("INDEX_GH_REPO",  "x9a-mem-2025-xpto")
BRANCH       = os.getenv("INDEX_GH_BRANCH","main")

# tenta inferir do Actions se não sobrescrever acima
repo_env = os.getenv("GITHUB_REPOSITORY", "")
if repo_env and (os.getenv("INDEX_GH_USER") is None or os.getenv("INDEX_GH_REPO") is None):
    try:
        user_env, repo_env_name = repo_env.split("/", 1)
        GITHUB_USER = user_env or GITHUB_USER
        REPO_NAME = repo_env_name or REPO_NAME
    except ValueError:
        pass

BASE_RAW = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/"

IGNORES_DIR = {".git", ".github", ".vercel", "__pycache__"}
IGNORES_FILE = {"index.json", ".DS_Store", "Thumbs.db"}

ROOT_DIR = os.path.abspath(os.getenv("GITHUB_WORKSPACE", "."))

def should_skip_dir(path):
    name = os.path.basename(path)
    return name in IGNORES_DIR

def should_skip_file(name):
    return name in IGNORES_FILE

def main():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # filtra dirs ignorados
        dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]
        for fn in filenames:
            if should_skip_file(fn):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT_DIR).replace("\\", "/")
            # pula o próprio index.json se existir na raiz
            if rel == "index.json":
                continue
            files.append({
                "path": rel,
                "url": BASE_RAW + rel
            })

    files.sort(key=lambda x: x["path"].lower())

    payload = {
        "version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "github": {"user": GITHUB_USER, "repo": REPO_NAME, "branch": BRANCH},
        "base_raw": BASE_RAW,
        "count": len(files),
        "files": files
    }

    out_path = os.path.join(ROOT_DIR, "index.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"[ok] index.json gerado com {len(files)} arquivos.")
    print(f"[info] base_raw = {BASE_RAW}")

if __name__ == "__main__":
    # garantir mimes mais comuns
    mimetypes.add_type("application/json", ".json")
    mimetypes.add_type("application/zip", ".zip")
    main()
