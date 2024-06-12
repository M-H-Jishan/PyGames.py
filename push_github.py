# Navigate to your project directory (if not already there)
C:\Users\User\Desktop\vs code.jishan\learn.py

# Initialize Git repository
git init

# Create a new README file and add initial content
echo "# 2d_Game.py" >> README.md

# Stage the README file for commit
git add README.md

# Commit the changes with a commit message
git commit -m "Initial commit"

# Rename the branch to 'main' (if it's not already named)
git branch -M main

# Add the remote repository URL (replace with your actual URL)
git remote add origin https://github.com/M-H-Jishan/2d_Game.py.git

# Push the committed changes to the 'main' branch on GitHub
git push -u origin main
