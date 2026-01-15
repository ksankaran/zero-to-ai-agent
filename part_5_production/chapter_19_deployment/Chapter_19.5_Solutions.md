## 19.5 Handling Concurrent Requests - Solutions

**Exercise 1 Solution:**

Here's how to load test your agent and interpret the results:

**Installing Load Testing Tools**

```bash
# Option 1: hey (Go-based, easy to install)
# On Mac:
brew install hey

# On Linux:
go install github.com/rakyll/hey@latest

# Option 2: ab (Apache Bench, often pre-installed)
# Comes with Apache, available on most systems
```

**Running Load Tests**

```bash
# Basic test: 20 requests, 5 concurrent
hey -n 20 -c 5 -m POST \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-key" \
    -d '{"message": "What is 2+2?"}' \
    http://localhost:8000/v1/chat

# Higher concurrency test
hey -n 50 -c 10 -m POST \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-key" \
    -d '{"message": "Hello"}' \
    http://localhost:8000/v1/chat

# Sustained load test (60 seconds)
hey -z 60s -c 5 -m POST \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-key" \
    -d '{"message": "Hi"}' \
    http://localhost:8000/v1/chat
```

**Sample Results and Interpretation**

```
Summary:
  Total:        45.2341 secs
  Slowest:      5.4521 secs
  Fastest:      1.2341 secs
  Average:      2.2617 secs
  Requests/sec: 0.4421
  
Response time histogram:
  1.234 [1]     |■■■■
  1.656 [3]     |■■■■■■■■■■■■
  2.078 [8]     |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  2.500 [5]     |■■■■■■■■■■■■■■■■■■■■
  2.922 [2]     |■■■■■■■■
  3.344 [1]     |■■■■

Status code distribution:
  [200] 20 responses
```

**What to Document**

```markdown
# Load Test Results

## Test Configuration
- Endpoint: POST /v1/chat
- Total Requests: 50
- Concurrency: 10
- Message: "What is 2+2?" (short, consistent)

## Results

### Baseline (5 concurrent)
- Average response time: 2.2s
- 95th percentile: 3.1s
- Requests/sec: 2.1
- Errors: 0

### Medium load (10 concurrent)
- Average response time: 3.8s
- 95th percentile: 5.2s
- Requests/sec: 2.5
- Errors: 0

### High load (20 concurrent)
- Average response time: 7.2s
- 95th percentile: 12.1s
- Requests/sec: 2.4
- Errors: 3 (timeouts)

## Observations
1. Response time increases significantly past 10 concurrent requests
2. Throughput (req/sec) plateaus around 2.5 - likely LLM API bottleneck
3. Timeouts start occurring at 20 concurrent (need to increase timeout or limit concurrency)

## Recommendations
- Set MAX_CONCURRENT_REQUESTS to 15
- Add semaphore to limit LLM calls
- Consider caching for common queries
```

---

**Exercise 2 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_2_19_5_solution.py`

```python
# Key pattern: Async queue with background workers
class RequestQueue:
    def __init__(self, max_concurrent: int = 5):
        self.requests: Dict[str, QueuedRequest] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self._lock = asyncio.Lock()
        self._workers_started = False
    
    async def enqueue(self, message: str) -> QueuedRequest:
        request_id = str(uuid.uuid4())
        async with self._lock:
            queued = QueuedRequest(
                id=request_id,
                message=message,
                status=RequestStatus.QUEUED,
                created_at=datetime.now(),
                position=self.queue.qsize() + 1
            )
            self.requests[request_id] = queued
            await self.queue.put(request_id)
        return queued
    
    async def worker(self):
        """Background worker processes queued requests."""
        while True:
            request_id = await self.queue.get()
            try:
                await self.process_request(request_id)
            finally:
                self.queue.task_done()
```

The full solution includes:
- `RequestStatus` enum (QUEUED, PROCESSING, COMPLETED, FAILED)
- `QueuedRequest` dataclass tracking status and position
- Background workers that process the queue
- Endpoints: POST `/v1/chat` (submit), GET `/v1/status/{id}` (check), GET `/v1/queue/stats`
- Cleanup function for old completed requests

**Usage Example:**

```bash
# Submit a request
curl -X POST http://localhost:8000/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me a story"}'

# Response:
# {"request_id": "abc-123", "status": "queued", "position": 1, "message": "..."}

# Check status
curl http://localhost:8000/v1/status/abc-123

# Response (while processing):
# {"request_id": "abc-123", "status": "processing", ...}

# Response (when done):
# {"request_id": "abc-123", "status": "completed", "result": "...", "processing_time_ms": 2341}
```

---

**Exercise 3 Solution:**

📥 **Download:** `part_5_production/chapter_19_deployment/exercise_3_19_5_solution.py`

```python
# Key pattern: Track active requests, wait for completion on shutdown
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
    
    async def request_finished(self):
        async with self._lock:
            self.active_requests -= 1
            if self.shutdown_requested and self.active_requests == 0:
                self._shutdown_event.set()
    
    async def wait_for_completion(self, timeout: float = 30.0):
        try:
            await asyncio.wait_for(self._shutdown_event.wait(), timeout=timeout)
            logger.info("All requests completed gracefully")
        except asyncio.TimeoutError:
            logger.warning(f"Shutdown timeout, {self.active_requests} requests still active")
```

The full solution includes:
- Signal handlers for SIGTERM and SIGINT
- Middleware that rejects new requests during shutdown
- Health endpoint that reports shutdown status
- Lifespan manager for startup/shutdown hooks
- HTTP client cleanup

**Testing Graceful Shutdown:**

```bash
# Terminal 1: Start the server
uvicorn exercise_3_19_5_solution:app --host 0.0.0.0 --port 8000

# Terminal 2: Send a slow request
curl -X POST http://localhost:8000/v1/chat &

# Terminal 2: Immediately trigger shutdown
curl http://localhost:8000/admin/shutdown

# Or send SIGTERM:
# kill -TERM <pid>

# Observe:
# - New requests get 503 response
# - In-progress request completes
# - Server shuts down after request finishes
```

**Expected Logs:**

```
INFO: Starting up...
INFO: HTTP client created
INFO: Signal handlers registered
INFO: Startup complete!
INFO: Shutdown requested, stopping new requests...
INFO: Waiting for active requests to complete...
INFO: All requests completed gracefully
INFO: HTTP client closed
INFO: Shutdown complete!
```

**Key Points:**

1. **Stop accepting new requests immediately** - Returns 503 to new requests
2. **Track in-progress requests** - Wait for them to complete
3. **Timeout for safety** - Don't wait forever for stuck requests
4. **Clean up resources** - Close HTTP clients, database connections, etc.
5. **Health endpoint reflects state** - Load balancers can route traffic away