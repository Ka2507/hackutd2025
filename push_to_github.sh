#!/bin/bash

# Helper script to push ProdigyPM to GitHub
# Run this manually: ./push_to_github.sh

echo "Pushing ProdigyPM to GitHub..."
echo "Repository: github.com/Ka2507/hackutd2025"
echo ""

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    echo "Remote 'origin' already configured"
else
    echo "Adding remote..."
    git remote add origin https://github.com/Ka2507/hackutd2025.git
fi

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "Success! Code pushed to:"
    echo "https://github.com/Ka2507/hackutd2025"
else
    echo ""
    echo "Push failed. You may need to:"
    echo "1. Authenticate with GitHub"
    echo "2. Check repository permissions"
    echo ""
    echo "Try running manually:"
    echo "  cd /Users/kaustubhannavarapu/ProdigyPM"
    echo "  git push -u origin main"
fi

