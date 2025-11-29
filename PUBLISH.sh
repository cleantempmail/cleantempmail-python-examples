#!/bin/bash
# Quick publish script for CleanTempMail Python Examples

echo "================================"
echo "Publishing to GitHub..."
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "cleantempmail.py" ]; then
    echo "❌ Error: Please run this script from the python-examples directory"
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📝 Adding files..."
git add .

# Ask for commit message
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update Python examples"
fi

echo "💾 Committing changes..."
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 Adding remote repository..."
    echo "Choose connection method:"
    echo "1) SSH (recommended)"
    echo "2) HTTPS"
    read -p "Enter choice (1 or 2): " method
    
    if [ "$method" = "1" ]; then
        git remote add origin git@github.com:cleantempmail/cleantempmail-python-examples.git
    else
        git remote add origin https://github.com/cleantempmail/cleantempmail-python-examples.git
    fi
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully published to GitHub!"
echo "🌐 View at: https://github.com/cleantempmail/cleantempmail-python-examples"
echo ""
