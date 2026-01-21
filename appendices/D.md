# Appendix D: Troubleshooting Guide

Building AI applications involves working with APIs, complex frameworks, and distributed systems. Things will go wrong - it's not a matter of if, but when. This appendix provides solutions to the most common issues you'll encounter while building LLM-powered applications, along with debugging strategies and performance optimization techniques.

---- 

## D.1 API Authentication Errors

Authentication errors are the most common issues when starting with LLM APIs. Here are the typical errors and their solutions:

| Error                                | Solution                                                                                                                                                                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **401: Invalid API Key**             | Check that your API key is correct and active: 1) Verify no extra spaces or quotes around the key, 2) Confirm the key hasn't been revoked in your dashboard, 3) Generate a new key if problems persist                   |
| **401: Organization Not Found**      | Your account may not be associated with an organization: 1) Check your organization settings in the provider dashboard, 2) Contact support or your organization admin                                                    |
| **API Key Not Found in Environment** | The environment variable isn't set correctly: 1) Verify your .env file exists and contains the key, 2) Ensure you're loading the .env file (use python-dotenv), 3) Check for typos in the variable name (case-sensitive) |

---- 

## D.2 Rate Limit Errors

Rate limiting protects API infrastructure from overload. Understanding the different types of rate limits helps you handle them appropriately:

| Error Code              | Meaning                                                              | Solution                                             |
| ----------------------- | -------------------------------------------------------------------- | ---------------------------------------------------- |
| 429: Too Many Requests  | You've exceeded requests per minute (RPM) or tokens per minute (TPM) | Implement exponential backoff; wait and retry        |
| 429: Quota Exceeded     | You've used all your credits or reached billing limit                | Add credits to your account; check billing settings  |
| 429: Rate Limit (burst) | Too many requests in a very short time window                        | Add delays between requests; batch requests together |

**Exponential Backoff Implementation:**

```python
import time
import random

def exponential_backoff(attempt, base_delay=1, max_delay=60):
    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
    time.sleep(delay)
    return delay
```

---- 

## D.3 Request Errors

| Error                       | Solution                                                                                                                                                                                                        |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **400: Bad Request**        | Your request format is invalid. Common causes: • Invalid JSON in the request body • Missing required parameters (model, messages) • Invalid parameter values (temperature \\\> 2.0)                             |
| **Context Length Exceeded** | Your input + output exceeds the model's context window: • Truncate or summarize conversation history • Use a model with larger context (GPT-4 Turbo: 128K) • Implement sliding window or summarization strategy |
| **404: Model Not Found**    | The specified model doesn't exist or you don't have access: • Check for typos in the model name • Verify the model is available in your region/tier • Check if the model has been deprecated                    |
| **500/503: Server Error**   | The API service is experiencing issues: • Check the provider's status page • Wait and retry with exponential backoff • Consider fallback to alternative provider                                                |

---- 

## D.4 Python Environment Issues

Environment issues are among the most frustrating to debug. Here are the most common problems and their solutions:

**ModuleNotFoundError: No module named 'xyz'**

This error means Python can't find the package. Common causes and solutions:

1. Package not installed: Run `pip install package-name`
2. Wrong virtual environment: Check `which python` points to your venv
3. Virtual environment not activated: Run `source venv/bin/activate`
4. Name conflict: Rename any local file named the same as the package

**error: externally-managed-environment**

This error (common on modern Linux/macOS) indicates the system Python is protected. Solutions:

- Create and use a virtual environment (recommended)
- Use `pip install --user package-name`
- Use pipx for CLI tools: `pipx install package-name`

**Virtual Environment Troubleshooting Checklist:**

```bash
# Verify you're in the right environment
which python           # Should show path to your venv
which pip              # Should match python path

# Check what's installed
pip list               # Show all installed packages
pip show package-name  # Show details for specific package

# If issues persist, recreate the environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---- 

## D.5 LangChain and Framework Errors

LangChain evolves rapidly, which can lead to import and compatibility issues:

| Error                                             | Solution                                                                                                                                                                                                                                                                   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ImportError: cannot import name 'X'**           | The import path has changed. LangChain reorganized packages: • Check the latest documentation for correct import paths • Common change: langchain → langchain\\\_community or langchain\\\_openai • Update packages: `pip install --upgrade langchain langchain-community` |
| **TypeError: issubclass() arg 1 must be a class** | Version mismatch between dependencies: • Update typing extensions: `pip install typing-inspect==0.8.0 typing_extensions==4.5.0` • Update pydantic: `pip install pydantic -U`                                                                                               |
| **Agent doesn't execute prompt**                  | Prompt template formatting issue: • Pass the formatted string, not the template object • Use `agent.run(prompt.format(input=value))`                                                                                                                                       |

---- 

## D.6 Debugging Strategies

Effective debugging is a systematic process. When something goes wrong, resist the urge to randomly change code. Instead, follow a structured approach.

**The Systematic Debugging Workflow**

Follow these steps in order when encountering any error:

**Step 1: Read the Error Message Carefully**

Error messages contain crucial information. Look for:
- Error type (e.g., TypeError, APIError, RateLimitError)
- Error message (describes what went wrong)
- Stack trace (shows where the error occurred)
- HTTP status codes for API errors (400, 401, 429, 500, etc.)

**Step 2: Reproduce the Issue**

Before fixing, ensure you can reliably reproduce the problem:
- Does it happen every time or intermittently?
- What specific inputs trigger it?
- Does it happen in isolation or only with certain code paths?

**Step 3: Isolate the Problem**

Narrow down where the issue occurs:
- Comment out sections to find the failing code
- Add print statements or logging to track execution
- Test components individually

**Step 4: Check the Basics**

Many issues stem from simple problems:
- Is your virtual environment activated?
- Are environment variables set correctly?
- Is your internet connection working?
- Are all dependencies installed and up to date?

**Effective Logging**

Good logging is essential for debugging LLM applications. Here's a practical setup:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()  # Also print to console
    ]
)

logger = logging.getLogger(__name__)

# Usage examples
logger.debug('Detailed info for debugging')   # Only shown when level=DEBUG
logger.info('General information')            # Normal operations
logger.warning('Something unexpected')        # Potential issues
logger.error('Something failed')              # Errors that need attention
logger.exception('Error with traceback')      # Includes full stack trace
```

**What to Log in LLM Applications:**

- API requests: model, token count, parameters used
- API responses: status, latency, token usage, finish reason
- Errors: full error message, request that caused it
- Agent decisions: tool selections, reasoning steps
- Performance metrics: response times, retry counts

**Debugging Tools and Techniques**

| Tool                    | Use Case                                                    | How to Use                                                      |
| ----------------------- | ----------------------------------------------------------- | --------------------------------------------------------------- |
| LangSmith               | Tracing LangChain applications; debugging chains and agents | Set LANGCHAIN\\\_TRACING\\\_V2=true and LANGCHAIN\\\_API\\\_KEY |
| Python Debugger (pdb)   | Step through code execution line by line                    | Add: `import pdb; pdb.set_trace()` at breakpoint                |
| VS Code Debugger        | Visual debugging with breakpoints and variable inspection   | Set breakpoints and press F5 to start debugging                 |
| Rich library            | Pretty-print complex objects and data structures            | `from rich import print; print(response)`                       |
| API Provider Dashboards | Monitor usage, errors, and rate limits                      | Check OpenAI/Anthropic usage pages regularly                    |

---- 

## D.7 Performance Optimization

LLM applications often suffer from latency and cost issues. Understanding where bottlenecks occur helps you optimize effectively.

**Latency Components**

| Component                  | Description                                 | Optimization Strategy                                   |
| -------------------------- | ------------------------------------------- | ------------------------------------------------------- |
| Time to First Token (TTFT) | Time until first response token is received | Use smaller models; reduce prompt length; use streaming |
| Inter-Token Latency        | Time between each generated token           | Hardware-dependent; use faster providers                |
| Network Latency            | Round-trip time to API servers              | Use regional endpoints; reduce request frequency        |
| Prompt Processing          | Time to process input tokens                | Shorter prompts; remove unnecessary context             |

**Key Latency Optimization Strategies:**

1. **Use streaming responses:** Users see responses immediately, improving perceived speed
2. **Choose the right model:** GPT-3.5 Turbo is ~6x faster than GPT-4; Claude Haiku is faster than Sonnet
3. **Optimize prompts:** Shorter, more focused prompts process faster
4. **Implement caching:** Cache common responses to avoid repeated API calls
5. **Parallelize when possible:** Use asyncio for concurrent API calls

**Token Usage and Cost Optimization**

*Reduce Input Tokens:*
- Trim unnecessary context from prompts
- Use summarization for long conversation histories
- Implement sliding window memory (keep only recent N messages)
- Use efficient system prompts (avoid repetition)

*Control Output Tokens:*
- Set appropriate max\_tokens limits
- Ask for concise responses in your prompt
- Use structured output formats (JSON is often more concise)

*Choose Cost-Effective Models:*
- Use GPT-3.5 Turbo or Claude Haiku for simple tasks
- Reserve GPT-4 or Claude Opus for complex reasoning
- Consider open-source models for high-volume, simple tasks

**Memory and Resource Management**

*Common Memory Issues:*
- Unbounded conversation history growing indefinitely
- Loading entire documents into memory for processing
- Caching too many embeddings in memory
- Not closing API connections properly

*Solutions:*
- Implement conversation pruning (keep last N messages)
- Use generators for large document processing
- Store embeddings in a vector database instead of memory
- Use context managers (with statements) for API clients

---- 

## D.8 Quick Reference Checklist

Use this checklist when encountering issues:

**Environment Issues:**
- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Python version is compatible (3.13+ recommended)
- [ ] No naming conflicts with local files

**API Issues:**
- [ ] API key is set and valid (no extra spaces/quotes)
- [ ] .env file exists and is being loaded
- [ ] Account has available credits/quota
- [ ] Internet connection is working
- [ ] API provider status is operational (check status page)

**Code Issues:**
- [ ] Model name is spelled correctly
- [ ] Required parameters are provided
- [ ] Parameter values are within valid ranges
- [ ] Error handling is implemented (try/except)

**Performance Issues:**
- [ ] Prompts are concise and focused
- [ ] Conversation history is pruned appropriately
- [ ] Appropriate model is selected for the task
- [ ] Caching is implemented where applicable

---- 

**Useful Status Pages:**

- **OpenAI:** [status.openai.com](https://status.openai.com)
- **Anthropic:** [status.claude.com](https://status.claude.com)
- **Google AI:** [status.cloud.google.com](https://status.cloud.google.com)

---- 

*Remember: Most problems have simple solutions. Start with the basics - check your environment, verify your API key, and read error messages carefully. When in doubt, create a minimal reproducible example and test each component in isolation.*