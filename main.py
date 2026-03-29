import os
import google.generativeai as genai
from github import Github

# 1. Setup
try:
    # Get environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number_str = os.getenv("PR_NUMBER")

    if not api_key or not github_token:
        raise ValueError("Missing API Keys in GitHub Secrets!")

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Configure GitHub
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number_str))

    print(f"Connected to PR #{pr_number_str} successfully.")

    # 2. Review Logic
    for file in pr.get_files():
        if file.filename.endswith('.py') and file.patch:
            print(f"Reviewing {file.filename}...")
            prompt = f"Act as a Senior AI Engineer. Review this code diff for DSA efficiency and security bugs: {file.patch}"
            
            response = model.generate_content(prompt)
            
            # Post the comment
            pr.create_issue_comment(f"### 🤖 AI Review for `{file.filename}`\n\n{response.text}")
            print(f"Comment posted for {file.filename}!")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)