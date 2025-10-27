# How to Push slackbench_real_sim to GitHub

## Quick Commands

Run these commands from the `SlackBench` directory:

```bash
# Navigate to SlackBench directory
cd /Users/jay./Desktop/Algoverse/SlackBench

# Initialize git (if not already)
cd slackbench_real_sim
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SlackBench real-time simulation"

# Add the remote repository
git remote add origin https://github.com/ovoxojxy/slack_simulation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step-by-Step Instructions

### 1. Initialize Git Repository
```bash
cd /Users/jay./Desktop/Algoverse/SlackBench/slackbench_real_sim
git init
```

### 2. Create .gitignore (Important!)
Before committing, create a `.gitignore` file:

```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
data/
*.log
.vscode/
.idea/
*.swp
*.swo
*~
```

### 3. Add and Commit Files
```bash
git add .
git commit -m "Initial commit: SlackBench real-time simulation with autonomous agents"
```

### 4. Connect to GitHub
```bash
git remote add origin https://github.com/ovoxojxy/slack_simulation.git
```

### 5. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## Important: Don't Commit Sensitive Data

**Before pushing, make sure your `.env` file is in `.gitignore`!**

The `.env` file contains:
- SLACK_BOT_TOKEN
- SLACK_APP_TOKEN  
- OPENAI_API_KEY

These should NEVER be committed to GitHub.

## If You Get Authentication Errors

If GitHub asks for authentication:

```bash
# Use a personal access token
# GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
# Create token with 'repo' scope
git push -u origin main
# When prompted, use the token as password
```

## Alternative: Using GitHub CLI

If you have `gh` installed:

```bash
gh repo create ovoxojxy/slack_simulation --public --source=.
git push -u origin main
```

## File Structure That Will Be Pushed

```
slackbench_real_sim/
├── README.md                      # Project overview
├── src/slack_io/                  # Core implementation
│   ├── agent_engine.py
│   ├── autonomous_loop.py
│   ├── bolt_app.py
│   ├── conductor.py
│   ├── persona_registry.py
│   ├── queue.py
│   └── slack_client.py
├── *.md                           # Documentation files
└── test_connection.py            # Startup script
```

## Quick Copy-Paste Commands

```bash
cd /Users/jay./Desktop/Algoverse/SlackBench/slackbench_real_sim
git init
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "data/" >> .gitignore
git add .
git commit -m "Initial commit: SlackBench real-time simulation"
git remote add origin https://github.com/ovoxojxy/slack_simulation.git
git branch -M main
git push -u origin main
```

