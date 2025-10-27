#!/bin/bash
# Quick script to push slackbench_real_sim to GitHub

echo "🚀 Pushing slackbench_real_sim to GitHub..."
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Initial commit: SlackBench real-time simulation with autonomous agents" || echo "No changes to commit"

# Add remote (won't error if already exists)
echo "🔗 Adding remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/ovoxojxy/slack_simulation.git

# Push to main
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your project is now on GitHub."
echo "🌐 View it at: https://github.com/ovoxojxy/slack_simulation"

