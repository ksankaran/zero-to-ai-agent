# Agent API

A production-ready conversational AI agent built with LangGraph and FastAPI.

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `uvicorn production_api:app --reload`

## Docker

Build and run with Docker:
```bash
docker build -t agent-api .
docker run -p 8000:8000 --env-file .env agent-api
```

## API Endpoints

- `GET /health` - Health check
- `POST /v1/chat` - Send a message to the agent

## Environment Variables

- `OPENAI_API_KEY` (required) - Your OpenAI API key
- `API_KEY` (optional) - API key for authentication
- `DEBUG` (optional) - Enable debug mode (default: false)
- `LOG_LEVEL` (optional) - Logging level (default: INFO)
- `PORT` (optional) - Server port (default: 8000)
- `MODEL_NAME` (optional) - OpenAI model (default: gpt-3.5-turbo)
- `MAX_TOKENS` (optional) - Max tokens per response (default: 1000)
