## 19.3 Deploying to Cloud Platforms - Solutions

**Exercise 1 Solution:**

This exercise requires you to actually deploy to a cloud platform. Here's what a successful completion looks like:

📥 **Download template:** `part_5_production/chapter_19_deployment/exercise_1_deployment_notes.md`

Your deployment notes should document:
- Platform chosen and rationale
- Configuration changes made
- Environment variables configured (names only, not values!)
- Public URL
- Verification test results

Example verification test:
```bash
curl -X POST "https://my-agent-production.up.railway.app/v1/chat" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: my-secret-key" \
     -d '{"message": "Hello from the cloud!"}'
```

---

**Exercise 2 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_2_19_3_solution.py`

```python
# Key pattern: Config dataclass with environment loading and validation
@dataclass
class Config:
    openai_api_key: str  # Required - no default
    api_key: str = "dev-key-change-in-production"
    debug: bool = False
    port: int = 8000
    
    @classmethod
    def from_environment(cls) -> "Config":
        # Try to load .env file in development
        env_file = Path(".env")
        if env_file.exists():
            cls._load_env_file(env_file)
        
        # Validate required settings
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ConfigurationError(
                "OPENAI_API_KEY is required. "
                "Set it in .env (local) or platform variables (production)."
            )
        return cls(openai_api_key=openai_key, ...)
```

The full solution includes:
- Dataclass with required and optional fields
- `from_environment()` classmethod that loads from .env locally
- Validation that fails fast with clear error messages
- Example FastAPI integration showing config usage

---

**Exercise 3 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_3_19_3_solution.md`

```markdown
# Deployment Guide - Key Sections

## Prerequisites
- GitHub account with repository pushed
- OpenAI API key
- Railway account (or preferred platform)

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| OPENAI_API_KEY | Yes | Your OpenAI API key |
| API_KEY | No | Authentication key (default: dev-key) |
...
```

The full DEPLOYMENT.md includes:
- Prerequisites checklist
- Environment variables table with descriptions
- Step-by-step instructions for Railway, Render, and manual Docker
- Verification commands and expected responses
- Rollback procedures
- Troubleshooting guide for common issues
- Support links

---

**Project Files (also in zip):**

📥 **Download:** `part_5_production/chapter_19_deployment/Dockerfile.deploy`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "production_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

📥 **Download:** `part_5_production/chapter_19_deployment/README_template.md`

```markdown
# Agent API
A production-ready conversational AI agent built with LangGraph and FastAPI.

## Setup
1. Copy `.env.example` to `.env` and fill in your API keys
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `uvicorn production_api:app --reload`
```

📥 **Download:** `part_5_production/chapter_19_deployment/env.example`

```
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional
API_KEY=your-api-key-for-authentication
DEBUG=false
LOG_LEVEL=INFO
PORT=8000
```

📥 **Download:** `part_5_production/chapter_19_deployment/gitignore.txt`

```
# Environment and secrets
.env
*.env.local

# Python
__pycache__/
venv/

# IDE and OS
.vscode/
.idea/
.DS_Store
```