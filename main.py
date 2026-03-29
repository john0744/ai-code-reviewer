import os
import google.generativeai as genai
from github import Github, Auth

def run_review():
    # 1. Capture Environment Variables
    api_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number_str = os.getenv("PR_NUMBER")

    # 2. Validation Check
    if not all([api_key, github_token, repo_name, pr_number_str]):
        print(f"Error: Missing variables. Key:{bool(api_key)}, Token:{bool(github_token)}, Repo:{repo_name}, PR:{pr_number_str}")
        return

    try:
        # 3. Setup Gemini (Using the most stable initialization)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 4. Setup GitHub (Using the modern Auth method to avoid DeprecationWarnings)
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number_str))

        print(f"🚀 Connected to {repo_name} PR #{pr_number_str}")

        # 5. Review Files
        for file in pr.get_files():
            if file.filename.endswith('.py') and file.patch:
                print(f"🔍 Analyzing {file.filename}...")
                
                prompt = (
                    f"Review the following Python code change for:\n"
                    f"1. Time Complexity (O-notation)\n"
                    f"2. Logical bugs or edge cases\n"
                    f"3. Security risks\n\n"
                    f"Code Diff:\n{file.patch}"
                )
                
                response = model.generate_content(prompt)
                
                # Post the AI response as a comment
                comment = f"### 🤖 AI Code Review: `{file.filename}`\n\n{response.text}"
                pr.create_issue_comment(comment)
                print(f"✅ Comment posted for {file.filename}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_review()