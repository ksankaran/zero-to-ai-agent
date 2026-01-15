#!/bin/bash
# From: Zero to AI Agent, Chapter 11, Section 11.2
# File: exercise_2_11_2_solution.sh

# Project setup automation script

echo "🚀 LangChain Project Setup Automation"
echo "======================================"

# Get project name
read -p "Enter project name: " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Project name required"
    exit 1
fi

# Create project directory
echo "📁 Creating project directory..."
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Create virtual environment
echo "🐍 Setting up virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✨ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || venv\Scripts\activate

# Install packages
echo "📦 Installing LangChain packages..."
pip install langchain langchain-openai python-dotenv

# Create project structure
echo "🏗️ Creating project structure..."
mkdir -p src tests data logs

# Create .env template
echo "📝 Creating .env template..."
cat > .env << EOF
# API Keys
OPENAI_API_KEY=your-key-here

# Settings
DEBUG_MODE=False
EOF

# Create .gitignore
echo "🔒 Creating .gitignore..."
cat > .gitignore << EOF
# Environment
.env
venv/
env/

# Python
__pycache__/
*.py[cod]
*\$py.class
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
EOF

# Create README
echo "📄 Creating README.md..."
cat > README.md << EOF
# $PROJECT_NAME

A LangChain project created with automated setup.

## Setup
1. Activate virtual environment: \`source venv/bin/activate\`
2. Add your API key to \`.env\`
3. Start building!

## Structure
- \`src/\` - Source code
- \`tests/\` - Test files
- \`data/\` - Data files
- \`logs/\` - Log files
EOF

# Create a test file
echo "🧪 Creating test file..."
cat > src/test_setup.py << EOF
from dotenv import load_dotenv
import os

load_dotenv()

if os.getenv("OPENAI_API_KEY"):
    print("✅ Setup complete! API key loaded.")
else:
    print("❌ Add your API key to .env file")
EOF

echo ""
echo "✅ Project '$PROJECT_NAME' created successfully!"
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Add your OpenAI API key to .env"
echo "3. Run: python src/test_setup.py"
echo ""
