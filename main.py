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
        # 1. Setup Modern Client
        client = genai.Client(api_key=api_key)

        # 2. Setup GitHub
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))

        print(f"🚀 Connected to {repo_name} PR #{pr_number}")

        for file in pr.get_files():
            if file.filename.endswith('.py') and file.patch:
                print(f"🔍 Analyzing {file.filename}...")
                
                # 3. USE THE FULL MODEL PATH
                # Adding 'models/' here is the "Silver Bullet" for 404 errors
                response = client.models.generate_content(
                    model='models/gemini-1.5-flash', 
                    contents=f"Review this Python code for bugs and O(n) complexity:\n\n{file.patch}"
                )
                
                # 4. Post the Comment
                comment_body = f"### 🤖 AI Code Review: `{file.filename}`\n\n{response.text}"
                pr.create_issue_comment(comment_body)
                print(f"✅ Comment posted successfully for {file.filename}")

    except Exception as e:
        # This will now print the FULL error so we can see if it's still a 404
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_review()