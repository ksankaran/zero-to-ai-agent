## 14.3 Installing and Setting Up LangGraph

**Exercise 1 Solution:**

Running `pip list` shows all installed packages. The exact count varies by system, but LangGraph typically installs 50-80 dependencies.

Some interesting dependencies include:

**tiktoken** - OpenAI's tokenizer library. It counts tokens (the units LLMs use to measure text length). This is crucial for staying within context limits and estimating costs.

**pydantic** - A data validation library. LangGraph uses it extensively to define and validate state schemas. When you create a TypedDict for your state, Pydantic ensures the data matches the expected types.

**aiohttp** - An asynchronous HTTP client. This enables LangGraph to make non-blocking API calls, which is important for parallel execution and responsive applications.

**tenacity** - A retry library. When API calls fail (rate limits, network issues), tenacity provides smart retry logic with exponential backoff. This makes your graphs more resilient.

**jsonpatch** - For applying partial updates to JSON objects. LangGraph uses this for efficient state updates—instead of replacing the entire state, it can apply just the changes.

---

**Exercise 2 Solution:**

We use a `.env` file instead of hardcoding API keys for several important reasons:

**Separation of configuration from code.** Your code describes *what* to do; configuration describes *how* to connect. These should be separate so you can change one without touching the other.

**Security through exclusion.** By adding `.env` to `.gitignore`, we ensure the key never enters version control. The code can be public while the secrets stay private.

**Easy environment switching.** Different environments (development, staging, production) can have different keys. With `.env` files, you just swap the file—no code changes needed.

**What could go wrong with a public API key:**

1. **Financial damage** - Anyone who finds your key can make API calls charged to your account. A malicious actor could run up thousands of dollars in charges overnight.

2. **Abuse for harmful content** - Your key could be used to generate harmful, illegal, or abusive content. This could get your account banned and potentially create legal liability.

3. **Rate limit exhaustion** - Even non-malicious use by others consumes your rate limits, preventing your actual application from working.

4. **Credential theft escalation** - Attackers often scan GitHub for API keys. Finding one key might lead them to probe for other vulnerabilities in your systems.

5. **Difficult recovery** - Once a key is in git history, it's there forever (even if you delete the file). You must revoke the key and generate a new one, then update all systems using it.

Real-world example: In 2023, researchers found over 10 million API keys and secrets exposed in public GitHub repositories. Many companies have faced significant financial losses from this.

---

**Exercise 3 Solution:**

📥 **Download:** `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_3_solution.py`

This comprehensive setup checker:
- Checks Python version compatibility (3.9+)
- Verifies all required packages are installed
- Tests LangGraph-specific imports
- Validates API key format
- Tests actual API connectivity
- Provides clear pass/fail summary
- Gives actionable fix instructions for failures
- Uses exit codes for scripting (0 = success, 1 = failure)

Key implementation pattern - checking packages dynamically:

```python
def check_packages():
    """Check all required packages are installed."""
    packages = {
        'langgraph': 'langgraph',
        'langchain': 'langchain', 
        'langchain_openai': 'langchain-openai',
        'dotenv': 'python-dotenv'
    }
    
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - run: pip install {package_name}")
```