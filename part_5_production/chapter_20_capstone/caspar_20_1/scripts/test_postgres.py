# From: Zero to AI Agent, Chapter 20, Section 20.1
# File: scripts/test_postgres.py

"""Quick test to verify PostgreSQL connection."""

import psycopg

# Connection string matching our docker-compose.yml
DATABASE_URL = "postgresql://caspar:caspar_secret@localhost:5432/caspar_db"

try:
    # Try to connect
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Run a simple query
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"✅ Connected to PostgreSQL!")
            print(f"   {version[:50]}...")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nMake sure PostgreSQL is running:")
    print("  docker compose up -d")
