import os
from github import Github

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if token:
            self.g = Github(token)
        else:
            self.g = None

    def create_pull_request(self, repo_name: str, branch_name: str, title: str, body: str, file_path: str, new_content: str):
        """Creates a new branch, commits the file, and opens a PR."""
        if not self.g:
            print("Warning: GITHUB_TOKEN not set. Mocking PR creation.")
            return True
            
        try:
            repo = self.g.get_repo(repo_name)
            source_branch = repo.get_branch("main")
            
            # Create branch
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
            
            # Update file
            file_contents = repo.get_contents(file_path, ref="main")
            repo.update_file(
                path=file_contents.path,
                message=f"Refactoring {file_path}",
                content=new_content,
                sha=file_contents.sha,
                branch=branch_name
            )
            
            # Create PR
            repo.create_pull(title=title, body=body, head=branch_name, base="main")
            return True
        except Exception as e:
            print(f"Failed to create PR: {e}")
            return False
