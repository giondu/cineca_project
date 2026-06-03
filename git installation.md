# step 1
sudo apt install git        # Debian/Ubuntu
sudo dnf install git        # Fedora

# step 2
git config --global user.name "Your Name"

git config --global user.email "your@email.com"

# step 3
cd /path/to/your/project
git init

git remote add origin https://github.com/youruser/yourproject.git

# Check what changed
git status

# Stage files you want to save
git add .                        # stage everything
git add src/myfile.py            # or stage specific files

# Commit with a message
git commit -m "describe what you did"

# Push to remote
git push origin main             # or 'master' depending on your branch name

# FINAL STEP
git push -u origin main

# Login request
Notice that git does not use te password anymore. You need to generate a PERSONAL TOKEN (GitHub > Settings > Developer Settings > Personal access tokens > Tokens (classic) >  Generate new token (classic) > Name and check the ``repo`` option > Click Generate token and copy it immediately (you won't see it again).)

At the ``push`` use the token as password.

To store the token as password, run the following:

git config --global credential.helper store

git push
