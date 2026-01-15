# Zero to AI Agent

**Learn Python and Build Intelligent Systems from Scratch**

Welcome to the code repository for *Zero to AI Agent*! This repository contains all the Python code examples, exercises, and projects from the book.

---

## 📁 Repository Structure

```
zero-to-ai-agent/
│
├── part_1_python/                    # Part I: Python Foundations
│   ├── chapter_01_setup/
│   ├── chapter_02_variables/
│   ├── chapter_03_control_flow/
│   ├── chapter_04_data_structures/
│   ├── chapter_05_functions/
│   └── chapter_06_external_data/
│
├── part_2_ai_fundamentals/           # Part II: AI and LLM Fundamentals
│   ├── chapter_07_intro_ai_llm/
│   ├── chapter_08_first_llm/
│   └── chapter_09_prompt_engineering/
│
├── part_3_building_agents/           # Part III: Building AI Agents
│   ├── chapter_10_what_are_agents/
│   ├── chapter_11_langchain_intro/
│   ├── chapter_12_tools_functions/
│   └── chapter_13_agent_memory/
│
├── part_4_langgraph/                 # Part IV: Advanced Agent Development
│   ├── chapter_14_langgraph_intro/
│   ├── chapter_15_stateful_agents/
│   ├── chapter_16_multi_agent/
│   └── chapter_17_advanced_patterns/
│
├── part_5_production/                # Part V: Production-Ready Agents
│   ├── chapter_18_testing/
│   ├── chapter_19_deployment/
│   └── chapter_20_capstone/
│
└── README.md                         # You are here!
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **VS Code** (or your preferred IDE)
- **Git** (to clone this repository)

### Clone the Repository

```bash
git clone https://github.com/ksankaran/zero-to-ai-agent.git
cd zero-to-ai-agent
```

---

## 🔧 Setting Up Virtual Environments

> ⚠️ **Important:** Each chapter should have its own virtual environment. This keeps dependencies isolated and prevents conflicts between chapters.

### Why Virtual Environments?

- **Isolation**: Each chapter's packages won't interfere with others
- **Reproducibility**: Ensures code works exactly as shown in the book
- **Clean setup**: Easy to delete and recreate if something goes wrong

---

### Step-by-Step Instructions

#### 1️⃣ Navigate to the Chapter Folder

```bash
# Example: Working on Chapter 2
cd part_1_python/chapter_02_variables
```

#### 2️⃣ Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

#### 3️⃣ Activate the Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

> ✅ You'll know it's activated when you see `(venv)` at the beginning of your terminal prompt.

#### 4️⃣ Install Chapter Dependencies

Most chapters include a `requirements.txt` file. Install the dependencies:

```bash
pip install -r requirements.txt
```

#### 5️⃣ Run the Code

```bash
python filename.py
```

#### 6️⃣ Deactivate When Done

```bash
deactivate
```

---

## 📋 Quick Reference Card

| Action | Windows | Mac/Linux |
|--------|---------|-----------|
| Create venv | `python -m venv venv` | `python3 -m venv venv` |
| Activate | `venv\Scripts\activate` | `source venv/bin/activate` |
| Deactivate | `deactivate` | `deactivate` |
| Install packages | `pip install -r requirements.txt` | `pip install -r requirements.txt` |

---

## 🆘 Troubleshooting

### "python" command not found
- **Windows**: Make sure Python is added to PATH during installation
- **Mac/Linux**: Try `python3` instead of `python`

### "venv\Scripts\activate" not working on PowerShell
Run this command first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Package installation fails
Make sure your virtual environment is activated (you should see `(venv)` in your prompt), then try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Virtual environment issues
Delete and recreate:
```bash
# Delete the venv folder
# Windows: rmdir /s /q venv
# Mac/Linux: rm -rf venv

# Then create a fresh one
python -m venv venv
```

---

## 🤝 Contributing

Found an error or want to improve the code? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b fix/chapter-2-typo`)
3. Commit your changes (`git commit -m 'Fix typo in chapter 2'`)
4. Push to the branch (`git push origin fix/chapter-2-typo`)
5. Open a Pull Request

---

## 📬 Contact

- **Author**: Kulanthaivelu Sankaran
- **Book Issues**: Open an issue in this repository

---

## 📄 License

This code is provided for educational purposes as a companion to *Zero to AI Agent*.

---

**Happy Coding! 🐍🤖**