import os
import google.generativeai as genai
from github import Github, Auth

def run_review():
    # 1. Capture Environment Variables
    api_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    if not all([api_key, github_token, repo_name, pr_number]):
        print("❌ Error: Missing environment variables.")
        return

    try:
        # 2. Setup Gemini - This configuration forces the stable v1 API
        genai.configure(api_key=api_key)
        
        # By not adding "models/" or using beta-specific flags, 
        # the newer library defaults to the stable endpoint.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 3. Setup GitHub
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))

        print(f"🚀 Connected to {repo_name} PR #{pr_number}")

        # 4. Review Files
        for file in pr.get_files():
            if file.filename.endswith('.py') and file.patch:
                print(f"🔍 Analyzing {file.filename}...")
                
                # Generate AI Review
                response = model.generate_content(
                    f"Act as a Senior AI Engineer. Review this code for DSA and bugs:\n\n{file.patch}"
                )
                
                # Post the Comment
                comment = f"### 🤖 AI Code Review: `{file.filename}`\n\n{response.text}"
                pr.create_issue_comment(comment)
                print(f"✅ Comment posted successfully for {file.filename}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_review()