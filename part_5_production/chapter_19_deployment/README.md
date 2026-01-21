# Chapter 19: Deployment and Scaling

## System Check

Before we begin, let's set up your workspace for this chapter:

1. Open VS Code

2. Open your terminal (Terminal → New Terminal)

3. Navigate to your project folder:

**On Windows:**
```
cd %USERPROFILE%\Desktop\ai_agents_complete
```

**On Mac/Linux:**
```
cd ~/Desktop/ai_agents_complete
```

4. Create a folder for this chapter:

**On Windows:**
```
mkdir part_5_production\chapter_19_deployment
cd part_5_production\chapter_19_deployment
```

**On Mac/Linux:**
```
mkdir -p part_5_production/chapter_19_deployment
cd part_5_production/chapter_19_deployment
```

5. Create and activate a virtual environment:

**On Windows:**
```
python -m venv venv
venv/Scripts/Activate.ps1
```

**On Mac/Linux:**
```
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

6. Install the required packages for Chapter 19:

> `part_5_production/chapter_19_deployment/requirements.txt`

Or copy and create the file yourself:

```
# requirements.txt
fastapi==0.124.0
uvicorn==0.38.0
openai==2.9.0
langgraph==1.0.4
langchain-core==1.2.0
python-dotenv==1.2.1
httpx==0.28.1
pydantic==2.12.5
```

Then install with:

```bash
pip install -r requirements.txt
```

This will install:
- `fastapi` (0.124.0) - modern web framework for building APIs
- `uvicorn` (0.38.0) - ASGI server to run FastAPI applications
- `openai` (2.9.0) - OpenAI Python SDK for LLM calls
- `langgraph` (1.0.4) - For building agent workflows with StateGraph
- `langchain-core` (1.2.0) - Core LangChain abstractions and interfaces
- `python-dotenv` (1.2.1) - for loading environment variables from .env files
- `httpx` (0.28.1) - async HTTP client for connection pooling
- `pydantic` (2.12.5) - data validation (also used by FastAPI)

7. Create your `.env` file with your API keys:

> `part_5_production/chapter_19_deployment/.env.example`

Or copy and create the file yourself:

```
# .env
# OpenAI API Key (required)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Rename `.env.example` to `.env` and replace with your actual API key.

**Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

8. **Install Docker** (required for section 19.1):

Docker is a tool that packages your application into a container. Visit https://docker.com/get-started and download Docker Desktop for your operating system. After installation, verify it's working:

```
docker --version
```

You should see something like `Docker version 24.0.7` (your version may differ).

> **Note**: Docker Desktop requires some system resources. If your computer is older or has limited RAM (less than 8GB), the Docker sections will still be valuable to read and understand - you can practice the concepts when you have access to a more powerful machine or use cloud-based alternatives.

You're all set! Let's start packaging your agents for the world.

---

## Practice Exercises

### Section 19.1

**Exercise 1: Build Your Own Container**

Create a Dockerfile for an agent you built in a previous chapter. Make sure to:
- Use a slim Python base image
- Generate requirements.txt with `pip freeze` (pinned versions)
- Add a non-root user
- Include a proper .gitignore

Test that it runs correctly with `docker run`.

> `part_5_production/chapter_19_deployment/exercise_1_19_1_solution.py`

**Exercise 2: Multi-Stage Optimization**

Take the Dockerfile from Exercise 1 and convert it to a multi-stage build. Compare the image sizes:
```bash
docker images
```

How much space did you save?

> `part_5_production/chapter_19_deployment/exercise_2_Dockerfile`

**Exercise 3: Docker Compose Development Setup**

Create a docker-compose.yml that:
- Builds your agent image
- Loads environment variables from a .env file
- Mounts your source code as a volume for easy development
- Exposes a port for future API access

Verify that changes to your Python code are reflected when you restart the container (without rebuilding).

> `part_5_production/chapter_19_deployment/exercise_3_docker-compose.yml`

---

### Section 19.2

**Exercise 1: Add a Conversations Endpoint**

Extend the API to include:
- `GET /v1/conversations` - List all conversation IDs
- `GET /v1/conversations/{id}` - Get messages for a specific conversation

You'll need to track conversation IDs and use `agent.get_state()` to retrieve history.

> `part_5_production/chapter_19_deployment/exercise_1_19_2_solution.py`

**Exercise 2: Add Input Validation**

Modify the chat endpoint to:
- Reject messages longer than 1000 characters
- Reject empty or whitespace-only messages
- Return appropriate error messages for each case

Use Pydantic validators or FastAPI's `Field` constraints.

> `part_5_production/chapter_19_deployment/exercise_2_19_2_solution.py`

**Exercise 3: Add Rate Limiting**

Implement a simple rate limiter that:
- Allows maximum 10 requests per minute per API key
- Returns a 429 (Too Many Requests) status when exceeded
- Includes a `Retry-After` header telling the client when to try again

> `part_5_production/chapter_19_deployment/exercise_3_19_2_solution.py`

---

### Section 19.3

**Exercise 1: Deploy Your Agent**

Take the agent API you built in section 19.2 and deploy it to a cloud platform. Document:
- Which platform you chose and why
- Any configuration changes you had to make
- The public URL of your deployed agent

Test it with curl from your local machine to verify it's working.

**Exercise 2: Environment Configuration**

Create a configuration system for your agent that:
- Works locally with a .env file
- Works in production with platform environment variables
- Has sensible defaults for optional settings
- Validates that required variables are present at startup

Your app should fail fast with a clear error message if `OPENAI_API_KEY` is missing, rather than crashing later with a confusing error.

> `part_5_production/chapter_19_deployment/exercise_2_19_3_solution.py`

```python
# Key pattern: Config dataclass with validation
@dataclass
class Config:
    openai_api_key: str  # Required - no default
    api_key: str = "dev-key-change-in-production"
    debug: bool = False
    port: int = 8000

    @classmethod
    def from_environment(cls) -> "Config":
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ConfigurationError("OPENAI_API_KEY is required.")
        # ... build config from environment
```

**Exercise 3: Deployment Documentation**

Create a `DEPLOYMENT.md` file for your project that documents:
- Prerequisites for deployment
- Step-by-step deployment instructions
- Required environment variables (with descriptions, not values)
- How to verify the deployment succeeded
- How to roll back if something goes wrong

Write it so that someone unfamiliar with your project could deploy it successfully.

> `part_5_production/chapter_19_deployment/exercise_3_19_3_solution.md`

---

### Section 19.4

**Exercise 1: Enhanced Logging**

Update your production API to include:
- JSON-formatted logs
- Request ID that's included in all log entries for a request
- Log the first 100 characters of the user's message (for debugging)
- Log the model used and token count (if available)

> `part_5_production/chapter_19_deployment/exercise_1_19_4_solution.py`

**Exercise 2: Metrics Dashboard**

Extend the `/metrics` endpoint to include:
- Requests per minute (last 5 minutes)
- 95th percentile response time
- Top 5 most common errors
- Token usage breakdown by conversation

> `part_5_production/chapter_19_deployment/exercise_2_19_4_solution.py`

**Exercise 3: Automated Alerts**

Implement an alerting system that:
- Sends an alert if error rate exceeds 20% in the last 10 requests
- Sends an alert if average response time exceeds 10 seconds
- Rate-limits alerts (no more than 1 alert per 5 minutes for the same issue)

> `part_5_production/chapter_19_deployment/exercise_3_19_4_solution.py`

---

### Section 19.5

**Exercise 1: Load Testing**

Use a tool like `hey` or `ab` (Apache Bench) to send multiple concurrent requests to your agent:

```bash
# Install hey: go install github.com/rakyll/hey@latest
hey -n 20 -c 5 -m POST \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-key" \
    -d '{"message": "Hello"}' \
    http://localhost:8000/v1/chat
```

Document:
- How many concurrent requests your agent handles before slowing down
- What errors occur under heavy load
- How response times change with load

**Exercise 2: Implement Request Queuing**

Create a queuing system that:
- Accepts requests even when the server is busy
- Processes them in order
- Returns a "request ID" immediately
- Provides a `/status/{request_id}` endpoint to check progress
- Returns results when ready

This pattern is useful for long-running agent tasks.

> `part_5_production/chapter_19_deployment/exercise_2_19_5_solution.py`

```python
# Key pattern: Background queue with status polling
class RequestQueue:
    def __init__(self, max_concurrent: int = 5):
        self.requests: Dict[str, QueuedRequest] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self._lock = asyncio.Lock()

    async def enqueue(self, message: str) -> QueuedRequest:
        request_id = str(uuid.uuid4())
        # ... create QueuedRequest, add to queue
        return queued

    async def get_status(self, request_id: str) -> Optional[QueuedRequest]:
        # Return current status and position in queue
        pass
```

**Exercise 3: Graceful Shutdown**

Implement graceful shutdown for your agent:
- Stop accepting new requests
- Wait for in-progress requests to complete (with a timeout)
- Clean up resources (close HTTP clients, flush logs)
- Exit cleanly

Test by sending requests while shutting down the server.

> `part_5_production/chapter_19_deployment/exercise_3_19_5_solution.py`

```python
# Key pattern: Track active requests, reject new ones during shutdown
class GracefulShutdown:
    def __init__(self):
        self.shutdown_requested = False
        self.active_requests = 0
        self._lock = asyncio.Lock()
        self._shutdown_event = asyncio.Event()

    async def request_started(self):
        async with self._lock:
            if self.shutdown_requested:
                raise RuntimeError("Server is shutting down")
            self.active_requests += 1

    async def wait_for_completion(self, timeout: float = 30.0):
        # Wait for active_requests to reach 0
        pass
```

---

### Section 19.6

**Exercise 1: Implement Smart Model Routing**

Create a model router that:
- Classifies requests into "simple," "medium," and "complex" categories
- Routes to gpt-4o-mini, gpt-4o, and gpt-4 respectively
- Logs which model was selected and why
- Tracks cost savings compared to always using gpt-4

Test with 20 varied requests and report the savings.

> `part_5_production/chapter_19_deployment/exercise_1_19_6_solution.py`

```python
# Key pattern: Classify complexity with patterns and heuristics
class SmartModelRouter:
    MODELS = {
        "simple": {"name": "gpt-4o-mini", "cost_per_1k": 0.0004},
        "medium": {"name": "gpt-4o", "cost_per_1k": 0.01},
        "complex": {"name": "gpt-4-turbo", "cost_per_1k": 0.02}
    }

    def classify_complexity(self, message: str) -> Tuple[str, str]:
        # Check simple patterns, complex patterns, then length
        # Returns (complexity, reason)
        pass

    def get_savings_report(self) -> dict:
        # Compare actual cost vs baseline (always GPT-4)
        pass
```

**Exercise 2: Build a Semantic Cache**

Improve the basic cache to use semantic similarity:
- Two messages don't need to be identical to get a cache hit
- "What's the weather?" and "How's the weather today?" should match
- Use embeddings to compare message similarity
- Set a similarity threshold for cache hits

Measure the improvement in cache hit rate.

> `part_5_production/chapter_19_deployment/exercise_2_19_6_solution.py`

```python
# Key pattern: Use embeddings for similarity matching
class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold
        self.entries: List[CacheEntry] = []

    def _get_embedding(self, text: str) -> List[float]:
        # Use text-embedding-3-small
        pass

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get(self, message: str) -> Optional[Tuple[str, float, bool]]:
        # Returns (response, similarity, is_exact_match)
        pass
```

**Exercise 3: Cost Dashboard**

Create a `/costs` endpoint that shows:
- Spending by hour for the last 24 hours
- Spending by model
- Top 10 most expensive conversations
- Projected monthly cost based on current usage
- Comparison to budget with visual indicator

Format the output as JSON suitable for a dashboard visualization.

> `part_5_production/chapter_19_deployment/exercise_3_19_6_solution.py`

```python
# Key pattern: Aggregate costs with multiple views
class CostDashboard:
    async def get_full_dashboard(self) -> Dict:
        return {
            "budget_status": await self.get_budget_status(),
            "hourly_spending": await self.get_hourly_spending(24),
            "spending_by_model": await self.get_spending_by_model(),
            "expensive_conversations": await self.get_expensive_conversations(10),
            "projections": await self.get_projected_monthly()
        }
```

---

### Section 19.7

**Exercise 1: Security Audit**

Audit your agent for security issues:
- Review all places where API keys are used
- Check all user inputs for validation
- Look for sensitive data in logs
- Test error messages for information leakage

Document what you find and create a remediation plan.

> `part_5_production/chapter_19_deployment/exercise_1_19_7_solution.py`

**Exercise 2: Prompt Injection Testing**

Test your agent's resistance to prompt injection:
- Try "Ignore all previous instructions..."
- Try "You are now an unfiltered AI..."
- Try to make the agent reveal its system prompt
- Try to make the agent produce inappropriate content

Document which attacks succeed and implement defenses.

> `part_5_production/chapter_19_deployment/exercise_2_19_7_solution.py`

**Exercise 3: Security Headers**

Add security headers to your API:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy` (if serving HTML)
- `Strict-Transport-Security` (HSTS)

Create middleware that adds these headers to all responses.

> `part_5_production/chapter_19_deployment/exercise_3_19_7_solution.py`
