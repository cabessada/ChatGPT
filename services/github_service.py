import os
from git import Repo

def setup_repo():
    repo = Repo(os.environ.get("REPO_PATH", "."))
    config_writer = repo.config_writer()
    config_writer.set_value("user", "name", os.environ.get("GIT_USER", "bot"))
    config_writer.set_value("user", "email", os.environ.get("GIT_EMAIL", "bot@localhost"))
    config_writer.release()
    return repo

def commit_and_push(commit_msg="Commit automático via API"):
    repo = setup_repo()
    repo.git.add(all=True)
    if repo.is_dirty():
        repo.index.commit(commit_msg)
        origin = repo.remote(name="origin")
        origin.push()
        return "Alterações enviadas"
    return "Nada para enviar"
