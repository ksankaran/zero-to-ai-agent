# Chapter 20: Capstone Project - CASPAR

**CASPAR** - Customer Assistance System for Product and Account Resolution

This folder contains all the code for the Chapter 20 capstone project.

---

## 📁 Folder Structure

```
chapter_20_capstone/
├── caspar/                 # ✅ COMPLETE PROJECT (reference only)
│
├── caspar_20_1/           # Section 20.1: Project Setup & Configuration
├── caspar_20_2/           # Section 20.2: Agent Architecture  
├── caspar_20_3/           # Section 20.3: Knowledge Base (RAG)
├── caspar_20_4/           # Section 20.4: Tools Integration
├── caspar_20_5/           # Section 20.5: Human Handoff
├── caspar_20_6/           # Section 20.6: Testing & Evaluation
└── caspar_20_7/           # Section 20.7: Deployment
```

---

## 📖 How to Follow Along

### Step 1: Create Your Working Folder

Before starting Section 20.1, create an empty `caspar` folder on your machine:

```bash
mkdir caspar
cd caspar
```

### Step 2: Copy Files As You Progress

As you complete each section in the book, copy the corresponding files from `caspar_20_X` into your `caspar` folder.

**⚠️ Important**: Copy individual files, not entire folders. Each section folder contains only the new files for that section.

```bash
# Example: After completing Section 20.1
cp caspar_20_1/pyproject.toml caspar/
cp caspar_20_1/requirements.txt caspar/
cp -r caspar_20_1/src caspar/
# ... etc

# Example: After completing Section 20.2
cp caspar_20_2/src/caspar/agent/nodes.py caspar/src/caspar/agent/
cp caspar_20_2/src/caspar/agent/graph.py caspar/src/caspar/agent/
# ... etc
```

### Step 3: Reference the Complete Version (Optional)

If you want to see how the finished project looks, or verify your work, check the `caspar/` folder in this repository. It contains the complete, working project.

---

## 📦 What Each Section Adds

| Section | Folder | Files Added |
|---------|--------|-------------|
| **20.1** | `caspar_20_1/` | Project structure, `config/settings.py`, `config/logging.py`, `pyproject.toml`, `requirements.txt` |
| **20.2** | `caspar_20_2/` | `agent/nodes.py`, `agent/graph.py`, `agent/state.py`, `agent/persistence.py` |
| **20.3** | `caspar_20_3/` | `knowledge/loader.py`, `knowledge/retriever.py`, `data/knowledge_base/*.md` |
| **20.4** | `caspar_20_4/` | `tools/orders.py`, `tools/accounts.py`, `tools/tickets.py`, updated `agent/nodes.py`, `agent/graph.py` |
| **20.5** | `caspar_20_5/` | `handoff/triggers.py`, `handoff/queue.py`, `handoff/context.py`, `agent/nodes_handoff_update.py`, `agent/graph_hitl.py` |
| **20.6** | `caspar_20_6/` | `tests/unit/*.py`, `tests/integration/*.py`, `tests/evaluation/*.py`, `tests/conftest.py` |
| **20.7** | `caspar_20_7/` | `Dockerfile`, `docker-compose.yml`, `api/main.py`, `api/metrics.py` |

---

## 🚀 Running the Complete Project

If you want to run the finished CASPAR agent directly:

```bash
# 1. Navigate to the complete project
cd caspar

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the API
uvicorn caspar.api.main:app --reload
```

---

## 🔧 Requirements

- Python 3.11+
- OpenAI API key
- Docker (for deployment, Section 20.7)
- PostgreSQL (optional, for production persistence)

### Key Dependencies

```
langchain==1.1.1
langgraph==1.0.4
langchain-chroma==1.0.0
fastapi==0.123.5
pydantic==2.12.5
```

See `requirements.txt` for the complete list.

---

## 📂 Complete Project Structure

```
caspar/
├── src/caspar/
│   ├── agent/           # LangGraph agent components
│   │   ├── nodes.py     # Node functions (classify, handle_*, respond)
│   │   ├── graph.py     # Graph construction
│   │   └── state.py     # AgentState definition
│   │
│   ├── knowledge/       # RAG system
│   │   ├── loader.py    # Document loading
│   │   └── retriever.py # ChromaDB retrieval
│   │
│   ├── tools/           # Customer service tools
│   │   ├── orders.py    # Order lookup
│   │   ├── accounts.py  # Account management
│   │   └── tickets.py   # Support tickets
│   │
│   ├── handoff/         # Human escalation
│   │   ├── triggers.py  # Escalation detection
│   │   └── queue.py     # Handoff queue
│   │
│   ├── api/             # FastAPI endpoints
│   │   ├── main.py      # API application
│   │   └── metrics.py   # Monitoring
│   │
│   └── config/          # Configuration
│       ├── settings.py  # Pydantic settings
│       └── logging.py   # Structured logging
│
├── tests/               # Test suite
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── data/
│   └── knowledge_base/  # FAQ and policy documents
│
├── scripts/             # Utility scripts
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

---

## 🧪 Running Tests

```bash
cd caspar

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/evaluation/

# Run with coverage
pytest --cov=caspar
```

---

## 🐳 Docker Deployment

```bash
cd caspar

# Start all services (API + PostgreSQL + Redis)
docker-compose up -d

# View logs
docker-compose logs -f caspar

# Stop services
docker-compose down
```

---

## ❓ Troubleshooting

**Import errors?**
```bash
pip install -e .  # Install the caspar package
```

**Missing API key?**
```bash
export OPENAI_API_KEY=sk-your-key-here
# Or add to .env file
```

---

## 📄 License

This code accompanies "Zero to AI Agent: Learn Python and Build Intelligent Systems from Scratch"