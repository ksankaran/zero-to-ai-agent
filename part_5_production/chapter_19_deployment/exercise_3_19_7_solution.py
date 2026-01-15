# Save as: exercise_3_19_7_solution.py
"""
Exercise 3 Solution: Security Headers Middleware

Adds essential security headers to all API responses.
Protects against common web attacks like XSS, clickjacking, and MIME sniffing.

Run: python exercise_3_19_7_solution.py
"""

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
import os


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    DEFAULT_HEADERS = {
        # Prevent MIME type sniffing
        "X-Content-Type-Options": "nosniff",
        
        # Prevent clickjacking
        "X-Frame-Options": "DENY",
        
        # Enable XSS filter
        "X-XSS-Protection": "1; mode=block",
        
        # Control referrer information
        "Referrer-Policy": "strict-origin-when-cross-origin",
        
        # Prevent content from being cached
        "Cache-Control": "no-store, no-cache, must-revalidate",
        "Pragma": "no-cache",
        
        # Remove server identification
        "Server": "Agent-API",
    }
    
    def __init__(
        self, 
        app,
        custom_headers: Optional[Dict[str, str]] = None,
        enable_hsts: bool = True,
        hsts_max_age: int = 31536000,  # 1 year
        enable_csp: bool = False,
        csp_policy: Optional[str] = None
    ):
        super().__init__(app)
        
        self.headers = self.DEFAULT_HEADERS.copy()
        
        if custom_headers:
            self.headers.update(custom_headers)
        
        # HSTS (HTTP Strict Transport Security)
        # Only enable in production with HTTPS
        if enable_hsts and os.getenv("ENVIRONMENT") == "production":
            self.headers["Strict-Transport-Security"] = f"max-age={hsts_max_age}; includeSubDomains"
        
        # Content Security Policy
        if enable_csp:
            default_csp = "default-src 'self'; script-src 'self'; style-src 'self'"
            self.headers["Content-Security-Policy"] = csp_policy or default_csp
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        for header, value in self.headers.items():
            response.headers[header] = value
        
        return response


class PermissionsPolicyMiddleware(BaseHTTPMiddleware):
    """
    Control browser features and APIs.
    
    Restricts access to potentially dangerous browser features.
    """
    
    def __init__(self, app, policy: Optional[Dict[str, str]] = None):
        super().__init__(app)
        
        default_policy = {
            "camera": "()",          # Deny camera access
            "microphone": "()",      # Deny microphone access
            "geolocation": "()",     # Deny geolocation
            "payment": "()",         # Deny payment API
            "usb": "()",             # Deny USB access
        }
        
        self.policy = policy or default_policy
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Build Permissions-Policy header
        policy_parts = [f"{k}={v}" for k, v in self.policy.items()]
        response.headers["Permissions-Policy"] = ", ".join(policy_parts)
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Validate and sanitize incoming requests.
    
    Checks content length and content type for security.
    """
    
    def __init__(self, app, max_content_length: int = 1_000_000):  # 1MB default
        super().__init__(app)
        self.max_content_length = max_content_length
    
    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length:
            if int(content_length) > self.max_content_length:
                return Response(
                    content='{"detail": "Request too large"}',
                    status_code=413,
                    media_type="application/json"
                )
        
        # Check content type for POST/PUT
        if request.method in ("POST", "PUT", "PATCH"):
            content_type = request.headers.get("content-type", "")
            if content_type and "application/json" not in content_type:
                # Allow form data for specific endpoints if needed
                if "/upload" not in str(request.url):
                    return Response(
                        content='{"detail": "Content-Type must be application/json"}',
                        status_code=415,
                        media_type="application/json"
                    )
        
        return await call_next(request)


def add_security_middleware(app: FastAPI) -> FastAPI:
    """
    Add all security middleware to the app.
    
    Usage:
        app = FastAPI()
        add_security_middleware(app)
    """
    # Order matters - last added is first executed
    app.add_middleware(RequestValidationMiddleware, max_content_length=1_000_000)
    app.add_middleware(PermissionsPolicyMiddleware)
    app.add_middleware(
        SecurityHeadersMiddleware,
        enable_hsts=True,
        enable_csp=True,
        csp_policy="default-src 'self'; frame-ancestors 'none'"
    )
    
    return app


# Verification script
def verify_security_headers(url: str) -> dict:
    """Check security headers on a URL."""
    import requests
    
    response = requests.get(url)
    headers = response.headers
    
    required_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": ["DENY", "SAMEORIGIN"],
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": None,  # Any value is OK
    }
    
    optional_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Permissions-Policy",
    ]
    
    results = {"passed": [], "failed": [], "optional": []}
    
    for header, expected in required_headers.items():
        if header in headers:
            if expected is None or headers[header] in (expected if isinstance(expected, list) else [expected]):
                results["passed"].append(f"✅ {header}: {headers[header]}")
            else:
                results["failed"].append(f"❌ {header}: Expected {expected}, got {headers[header]}")
        else:
            results["failed"].append(f"❌ {header}: Missing")
    
    for header in optional_headers:
        if header in headers:
            results["optional"].append(f"✅ {header}: {headers[header]}")
        else:
            results["optional"].append(f"⚠️ {header}: Not set (optional)")
    
    return results


# Example FastAPI app with all security middleware
app = FastAPI(title="Secure Agent API")

# Add all security middleware
add_security_middleware(app)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/test-headers")
async def test_headers():
    """Endpoint to verify security headers."""
    return {"message": "Check the response headers!"}


@app.post("/v1/chat")
async def chat(message: str = "Hello"):
    """Protected chat endpoint."""
    return {"response": f"Echo: {message}"}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        # Verify mode - check headers on a running server
        url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000/health"
        
        print(f"🔍 Checking security headers for: {url}\n")
        
        try:
            results = verify_security_headers(url)
            
            print("Required Headers:")
            for item in results["passed"] + results["failed"]:
                print(f"  {item}")
            
            print("\nOptional Headers:")
            for item in results["optional"]:
                print(f"  {item}")
            
            passed = len(results["passed"])
            total = passed + len(results["failed"])
            print(f"\nScore: {passed}/{total} required headers")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure the server is running!")
    
    else:
        # Server mode - run the app
        import uvicorn
        
        print("Security Headers Demo Server")
        print("=" * 50)
        print("Endpoints:")
        print("  GET  /health       - Health check")
        print("  GET  /test-headers - Test security headers")
        print("  POST /v1/chat      - Chat endpoint")
        print("\nTo verify headers, run in another terminal:")
        print("  python exercise_3_19_7_solution.py verify http://localhost:8000/health")
        print("  curl -I http://localhost:8000/health")
        print("=" * 50 + "\n")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
