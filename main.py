import os
import google.generativeai as genai
from github import Github

# 1. Configuration & Setup
try:
    # Fetch secrets from environment variables
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    GH_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO_NAME = os.getenv("GITHUB_REPOSITORY")
    PR_NUM = os.getenv("PR_NUMBER")

    if not all([GEMINI_KEY, GH_TOKEN, REPO_NAME, PR_NUM]):
        print("ERROR: One or more environment variables are missing.")
        exit(1)

    # Initialize Gemini
    genai.configure(api_key=GEMINI_KEY)
    ai_model = genai.GenerativeModel('gemini-1.5-flash')

    # Initialize GitHub
    git_client = Github(GH_TOKEN)
    target_repo = git_client.get_repo(REPO_NAME)
    pull_req = target_repo.get_pull(int(PR_NUM))

    print(f"Successfully connected to {REPO_NAME} PR #{PR_NUM}")

except Exception as setup_err:
    print(f"SETUP CRITICAL ERROR: {setup_err}")
    exit(1)

# 2. Review Execution
for file in pull_req.get_files():
    # Only review Python files that have actual changes (a 'patch')
    if file.filename.endswith('.py') and file.patch:
        print(f"AI is analyzing: {file.filename}...")
        try:
            prompt = (
                "Act as a Senior Software Engineer. Review the following code change (diff) "
                "for logic errors, security risks, and time complexity issues. "
                f"File: {file.filename}\n\n{file.patch}"
            )
            
            ai_response = ai_model.generate_content(prompt)
            
            # Post the AI's feedback as a comment on the PR
            comment_body = f"### 🤖 AI Code Review: `{file.filename}`\n\n{ai_response.text}"
            pull_req.create_issue_comment(comment_body)
            print(f"Comment posted for {file.filename}")

        except Exception as ai_err:
            print(f"ERROR DURING AI REVIEW FOR {file.filename}: {ai_err}")

print("Review process completed.")