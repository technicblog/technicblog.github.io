#!/bin/bash
set -euo pipefail

#Change to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
cd "$SCRIPT_DIR"

#Set variables for Obsidian to Hugo copy
sourcePath="/var/home/deck/Documents/Vault/posts"
destinationPath="/home/deck/Documents/techno/content/posts"

#Set GitHub Repo
myrepo="git@github.com:technicblog/technicblog.github.io.git"

#Check for required commands
for cmd in git rsync python3 hugo; do
if ! command -v $cmd &> /dev/null; then
echo "$cmd is not installed or not in PATH."
exit 1
fi
done

#Step 1: Check if Git is initialized, and initialize if necessary
if [ ! -d ".git" ]; then
echo "Initializing Git repository..."
git init
git remote add origin $myrepo
else
echo "Git repository already initialized."
if ! git remote | grep -q 'origin'; then
echo "Adding remote origin..."
git remote add origin $myrepo
fi
fi

#Step 2: Sync posts from Obsidian to Hugo content folder using rsync
echo "Syncing posts from Obsidian..."

if [ ! -d "$sourcePath" ]; then
echo "Source path does not exist: $sourcePath"
exit 1
fi

if [ ! -d "$destinationPath" ]; then
echo "Destination path does not exist: $destinationPath"
exit 1
fi

rsync -av --delete "$sourcePath" "$destinationPath"

#Step 3: Process Markdown files with Python script to handle image links
echo "Processing image links in Markdown files..."
if [ ! -f "images.py" ]; then
echo "Python script images.py not found."
exit 1
fi

if ! python3 images.py; then
echo "Failed to process image links."
exit 1
fi

#Step 4: Build the Hugo site
echo "Building the Hugo site..."
if ! hugo; then
echo "Hugo build failed."
exit 1
fi

# Step 5: Add all changes
echo "Staging all changes..."
git add .

# Step 6: Always commit on first run, otherwise only if changes
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    if ! git diff --cached --quiet; then
        commit_message="New Blog Post on $(date +'%Y-%m-%d %H:%M:%S')"
        git commit -m "$commit_message"
    else
        echo "No new changes to commit."
    fi
else
    echo "Initial commit..."
    git commit -m "Initial Hugo site with First Post"
fi

# Step 7: Push to master (your branch name)
echo "Deploying to GitHub Pages..."
git push origin master:main --force

echo "All done! Site synced, processed, committed, built, and pushed to main. GitHub Actions will deploy to GitHub Pages automatically."
