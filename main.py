from github import Github
import os
import get_ai_review
# Purpose: Authenticate with GitHub using the token provided by the Action
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))

# Purpose: Get the changes from the latest Pull Request
pull_request = repo.get_pull(int(os.getenv("PR_NUMBER")))
commits = pull_request.get_commits()

for commit in commits:
    for file in commit.files:
        # Send the file changes to our AI Brain
        review = get_ai_review(file.patch)
        # Purpose: Post the result as a comment on the PR
        pull_request.create_issue_comment(f"AI Review for {file.filename}:\n{review}")