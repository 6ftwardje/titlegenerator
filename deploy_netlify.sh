#!/bin/bash

# Cryptoriez Short Titler & Describer - Netlify Deployment Script
# This script helps prepare and deploy your application to Netlify

echo "🚀 Cryptoriez Short Titler & Describer - Netlify Deployment"
echo "=========================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Initializing..."
    git init
    echo "✅ Git repository initialized"
fi

# Check if files exist
echo "📁 Checking required files..."
required_files=("index.html" "styles.css" "script.js" "netlify.toml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files: ${missing_files[*]}"
    echo "Please ensure all files are present before deploying."
    exit 1
fi

echo "✅ All required files found"

# Add all files to git
echo "📝 Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Update for Netlify deployment - $(date)"
    echo "✅ Changes committed"
fi

# Check if remote origin exists
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  No remote origin found. You'll need to add one manually:"
    echo "   git remote add origin <your-repo-url>"
    echo ""
    echo "📋 For now, you can deploy manually by:"
    echo "   1. Going to netlify.com"
    echo "   2. Dragging this folder to the deploy area"
    echo "   3. Your site will be live instantly!"
else
    echo "🌐 Remote origin found: $(git remote get-url origin)"
    echo "📤 Pushing to remote..."
    if git push origin main; then
        echo "✅ Code pushed successfully!"
        echo ""
        echo "🎉 Next steps:"
        echo "   1. Go to netlify.com"
        echo "   2. Click 'New site from Git'"
        echo "   3. Choose your repository"
        echo "   4. Click 'Deploy site'"
        echo ""
        echo "Your site will be live in minutes!"
    else
        echo "❌ Failed to push to remote"
        echo "You can still deploy manually by dragging this folder to Netlify"
    fi
fi

echo ""
echo "🔗 Netlify will automatically detect your settings from netlify.toml"
echo "📱 Your app will be fully responsive and work on all devices"
echo ""
echo "Happy deploying! 🚀"
