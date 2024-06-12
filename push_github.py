# -*- coding: utf-8 -*-
import git

# Local path to your project directory
project_dir = r"C:\Users\User\Desktop\vs code.jishan\learn.py"

# URL of the specific GitHub repository you want to push to
repo_url = "https://github.com/M-H-Jishan/2d_Game.py.git"

# Initialize a git repository object
repo = git.Repo(project_dir)

# Add all files to the staging area
repo.git.add(".")

# Commit the changes
repo.git.commit("-m", "Initial commit")

# Set the remote URL for your repository
origin = repo.create_remote('origin', repo_url)

# Push your changes to GitHub
origin.push()

print("Project pushed to GitHub successfully.")
