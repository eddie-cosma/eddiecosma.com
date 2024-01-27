import json
import shutil
from pathlib import Path

import git
from flask import Flask, request

app = Flask(__name__)

@app.route("/update", methods=['POST'])
def update():
    github_data = request.get_json()
    if github_data.get("repository", {}).get("name") == "eddiecosma.com":
        www_dir = Path('/www')
        tmp_dir = Path('/tmp/www')
        target_subdir = 'website/public'

        if not www_dir.exists():
            print("FATAL: The webroot must be mounted to /www")
            return "Update failed"

        for item in www_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        
        repo_url = "https://github.com/eddie-cosma/eddiecosma.com"
        git.Repo.clone_from(repo_url, tmp_dir)
        # Copy only the contents of the public subdirectory to webroot
        shutil.copytree(
            src=tmp_dir / target_subdir,
            dst=www_dir,
            symlinks=False,
            ignore=None,
            dirs_exist_ok=True
        )
        return "Update completed"

    return "Update failed"
