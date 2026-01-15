## 19.1 Containerizing Your Agent with Docker

**Exercise 1 Solution:**

Here's a complete example containerizing a research agent with all required features.

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_1_19_1_solution.py`

The solution creates a two-node research agent that gathers facts and summarizes them:

```python
class ResearchState(TypedDict):
    topic: str
    findings: Annotated[list[str], operator.add]
    summary: str

def research_topic(state: ResearchState) -> ResearchState:
    """Research the given topic."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = f"Provide 3 key facts about: {state['topic']}"
    response = llm.invoke(prompt)
    return {"findings": response.content.split("\n")}
```

Generate requirements with `pip freeze > requirements.txt`, then build and run:

```bash
docker build -t research-agent:v1 .
docker run --env OPENAI_API_KEY=your-key research-agent:v1
```

---

**Exercise 2 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_2_Dockerfile`

The multi-stage build separates dependency installation from the runtime image:

```dockerfile
# Stage 1: Builder - install dependencies
FROM python:3.13-slim as builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime - only what we need
FROM python:3.13-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```

To compare image sizes:

```bash
# Build single-stage version
docker build -t research-agent:single -f Dockerfile.single .

# Build multi-stage version
docker build -t research-agent:multi .

# Compare sizes
docker images | grep research-agent
```

Example output:
```
research-agent   single   abc123   5 minutes ago   412MB
research-agent   multi    def456   2 minutes ago   287MB
```

The multi-stage build saves approximately 30% of space.

---

**Exercise 3 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_3_docker-compose.yml`

The development docker-compose.yml mounts source code for live editing:

```yaml
version: '3.8'
services:
  agent:
    build: .
    env_file:
      - .env
    volumes:
      - ./research_agent.py:/app/research_agent.py
    ports:
      - "8000:8000"
    stdin_open: true
    tty: true
```

To verify changes are reflected without rebuilding:

1. Start the container: `docker-compose up -d`
2. Check current output: `docker-compose logs agent`
3. Edit `research_agent.py` (change the topic or add a print statement)
4. Restart: `docker-compose restart agent`
5. Check logs again: `docker-compose logs agent`

The changes appear without rebuilding because the volume mount makes your local file visible inside the container.

Note: For Python applications, you'll still need to restart the container to pick up code changes (Python loads modules once at startup). For true hot-reloading, you'd use a web framework's development server with auto-reload enabled.