import os
from google import genai
from github import Github, Auth

def run_review():
    api_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    if not all([api_key, github_token, repo_name, pr_number]):
        print("❌ Error: Missing environment variables.")
        return

    try:
        # 1. Setup Client and FORCE v1 (Stable) API
        client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1'}
        )

        # 2. Setup GitHub
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))

        print(f"🚀 Connected to {repo_name} PR #{pr_number}")

        for file in pr.get_files():
            if file.filename.endswith('.py') and file.patch:
                print(f"🔍 Analyzing {file.filename}...")
                
                # 3. USE 'gemini-1.5-flash' (No prefix) with v1 Stable
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"Review this Python code for bugs and DSA complexity:\n\n{file.patch}"
                )
                
                # 4. Post the Comment
                comment = f"### 🤖 AI Code Review: `{file.filename}`\n\n{response.text}"
                pr.create_issue_comment(comment)
                print(f"✅ Comment posted successfully!")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_review()