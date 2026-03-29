import os
import google.generativeai as genai
from github import Github

# 1. Configuration
# These MUST match the names in your .yml file exactly
api_key = os.getenv("GEMINI_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_num_str = os.getenv("PR_NUMBER")

# Debugging: Tell us what is missing
if not api_key: print("MISSING: GEMINI_API_KEY")
if not github_token: print("MISSING: GITHUB_TOKEN")
if not repo_name: print("MISSING: GITHUB_REPOSITORY")
if not pr_num_str: print("MISSING: PR_NUMBER")

if not all([api_key, github_token, repo_name, pr_num_str]):
    exit(1)

# 2. Setup
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
g = Github(github_token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_num_str))

# 3. Review
for file in pr.get_files():
    if file.filename.endswith('.py') and file.patch:
        print(f"Reviewing {file.filename}...")
        prompt = f"Review this Python code for bugs and O(n) complexity: {file.patch}"
        response = model.generate_content(prompt)
        pr.create_issue_comment(f"### 🤖 AI Review for `{file.filename}`\n\n{response.text}")

print("Done!")