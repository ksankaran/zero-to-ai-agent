# CASPAR - Complete Project Structure

## Final Project Layout (58 files)

```
caspar/
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Local development setup
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
│
├── data/
│   └── knowledge_base/
│       ├── faq.md                  # General FAQ content
│       ├── policies.md             # Return/shipping policies
│       ├── products.md             # Product information
│       └── troubleshooting.md      # Common issues & solutions
│
├── scripts/
│   ├── build_knowledge_base.py     # Initialize ChromaDB
│   ├── run_tests.py                # Unified test runner
│   ├── test_conversation_flow.py   # Manual conversation testing
│   ├── test_handoff.py             # Manual handoff testing
│   └── verify_setup.py             # Environment verification
│
├── src/
│   ├── __init__.py
│   └── caspar/
│       ├── __init__.py             # Package init (version)
│       │
│       ├── agent/                  # Core agent logic
│       │   ├── __init__.py         # Exports create_agent, create_initial_state
│       │   ├── graph.py            # LangGraph workflow with HITL
│       │   ├── nodes.py            # Processing nodes (classify, respond, etc.)
│       │   ├── persistence.py      # Checkpoint persistence
│       │   └── state.py            # AgentState TypedDict
│       │
│       ├── api/                    # REST API layer
│       │   ├── __init__.py         # Exports app, metrics
│       │   ├── main.py             # FastAPI application
│       │   └── metrics.py          # Simple metrics collector
│       │
│       ├── config/                 # Configuration
│       │   ├── __init__.py         # Exports settings, get_logger
│       │   ├── logging.py          # Structured logging setup
│       │   ├── logging_config.py   # Production JSON logging
│       │   └── settings.py         # Pydantic settings
│       │
│       ├── handoff/                # Human escalation system
│       │   ├── __init__.py         # Exports all handoff components
│       │   ├── approval.py         # Human approval workflow
│       │   ├── context.py          # Context builder for agents
│       │   ├── notifications.py    # Alert notifications
│       │   ├── queue.py            # Handoff queue management
│       │   └── triggers.py         # Escalation trigger detection
│       │
│       ├── knowledge/              # RAG system
│       │   ├── __init__.py         # Exports get_retriever
│       │   ├── loader.py           # Document loading
│       │   └── retriever.py        # ChromaDB retrieval
│       │
│       └── tools/                  # Business tools
│           ├── __init__.py         # Exports convenience functions
│           ├── accounts.py         # Account lookup tool
│           ├── orders.py           # Order lookup tool
│           └── tickets.py          # Ticket creation tool
│
└── tests/
    ├── __init__.py
    ├── conftest.py                 # Shared pytest fixtures
    │
    ├── evaluation/                 # Quality evaluation
    │   ├── __init__.py
    │   ├── evaluator.py            # LLM-as-judge framework
    │   ├── run_dataset_evaluation.py  # Batch evaluation runner
    │   ├── test_dataset.py         # Test cases dataset
    │   └── test_response_quality.py   # Quality score tests
    │
    ├── integration/                # Full conversation tests
    │   ├── __init__.py
    │   ├── test_conversation_flows.py  # End-to-end flows
    │   ├── test_edge_cases.py      # Edge case handling
    │   └── test_intent_classification.py  # Intent accuracy
    │
    └── unit/                       # Component tests
        ├── __init__.py
        ├── test_handoff_triggers.py    # Escalation trigger tests
        ├── test_tools_convenience.py   # Convenience function tests
        ├── test_tools_orders.py        # Order tool tests
        └── test_tools_tickets.py       # Ticket tool tests
```

## File Count by Section

| Section | Files | Description |
|---------|-------|-------------|
| 20.1 Project Setup | 10 | Config, settings, logging, directory structure |
| 20.2 Agent Architecture | 6 | State, nodes, graph, persistence |
| 20.3 Knowledge Retrieval | 10 | Loader, retriever, FAQ documents, scripts |
| 20.4 Conversation Flow | 8 | Tools (orders, tickets, accounts), updated nodes/graph |
| 20.5 Human Handoff | 9 | Triggers, queue, context, notifications, approval |
| 20.6 Testing | 17 | Unit, integration, evaluation tests, fixtures |
| 20.7 Deployment | 7 | Dockerfile, docker-compose, API, metrics |

**Total: 67 files** (some files updated across sections)

## Key Components

### Agent Core (Section 20.2)
- **state.py**: Defines `AgentState` TypedDict with all conversation fields
- **nodes.py**: Processing functions (classify_intent, check_escalation, generate_response, etc.)
- **graph.py**: LangGraph `StateGraph` with conditional routing and human-in-the-loop

### Knowledge Base (Section 20.3)
- **retriever.py**: ChromaDB-based semantic search
- **loader.py**: Markdown document parsing with metadata
- **data/knowledge_base/*.md**: FAQ, policies, products, troubleshooting

### Tools (Section 20.4)
- **orders.py**: `OrderLookupTool` with mock order database
- **tickets.py**: `TicketTool` for creating support tickets
- **accounts.py**: `AccountTool` for customer info lookup

### Handoff System (Section 20.5)
- **triggers.py**: Detects escalation conditions (frustration, VIP, sensitive topics)
- **queue.py**: Manages handoff queue with priority
- **context.py**: Builds comprehensive handoff summaries
- **notifications.py**: Multi-channel alerts (console, email, Slack)

### Testing (Section 20.6)
- **Unit tests**: Fast, no LLM calls, test individual components
- **Integration tests**: Full flows with real LLM
- **Evaluation tests**: LLM-as-judge for quality scoring

### Deployment (Section 20.7)
- **Dockerfile**: Production container with health checks
- **docker-compose.yml**: Local development with Redis
- **api/main.py**: FastAPI with lifespan, CORS, metrics
- **api/metrics.py**: Thread-safe metrics collector

## Running the Project

```bash
# Setup
cd caspar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Build knowledge base
python scripts/build_knowledge_base.py

# Run tests
python scripts/run_tests.py --suite unit    # Fast
python scripts/run_tests.py --suite all     # Complete

# Start API
uvicorn caspar.api.main:app --reload

# Or with Docker
docker-compose up --build
```

## Architecture Diagram

```
┌────────────────────────────────────────────────────────────┐
│                      CASPAR Agent                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────────┐   │
│  │ Classify │──▶│ Check Escal. │──▶│ Route by Intent   │   │
│  │  Intent  │   │  Triggers    │   │                   │   │
│  └──────────┘   └──────────────┘   └───────────────────┘   │
│                                           │                │
│         ┌─────────────────────────────────┼────────────┐   │
│         ▼              ▼                  ▼            ▼   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐   │
│  │    FAQ    │  │   Order   │  │ Complaint │  │ Handoff│   │
│  │  Handler  │  │  Handler  │  │  Handler  │  │  Node  │   │
│  └───────────┘  └───────────┘  └───────────┘  └────────┘   │
│         │              │              │            │       │
│         ▼              ▼              ▼            ▼       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐   │
│  │ Knowledge │  │   Order   │  │  Ticket   │  │  Human │   │
│  │   Base    │  │   Tool    │  │   Tool    │  │  Agent │   │
│  └───────────┘  └───────────┘  └───────────┘  └────────┘   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```