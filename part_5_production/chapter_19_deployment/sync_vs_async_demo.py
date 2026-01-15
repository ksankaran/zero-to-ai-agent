# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: sync_vs_async_demo.py
# Description: Demonstrates the difference between sync and async execution

import asyncio
import time


def sync_task(name: str, duration: float) -> str:
    """Synchronous task - blocks everything."""
    print(f"{name}: Starting")
    time.sleep(duration)  # Blocks the entire program
    print(f"{name}: Done")
    return f"{name} result"


async def async_task(name: str, duration: float) -> str:
    """Async task - allows other work during wait."""
    print(f"{name}: Starting")
    await asyncio.sleep(duration)  # Yields control during wait
    print(f"{name}: Done")
    return f"{name} result"


# Synchronous version - runs sequentially
def run_sync():
    start = time.time()
    sync_task("A", 1)
    sync_task("B", 1)
    sync_task("C", 1)
    print(f"Sync total: {time.time() - start:.1f}s")


# Async version - runs concurrently
async def run_async():
    start = time.time()
    await asyncio.gather(
        async_task("A", 1),
        async_task("B", 1),
        async_task("C", 1)
    )
    print(f"Async total: {time.time() - start:.1f}s")


if __name__ == "__main__":
    # Run both versions to compare
    print("=== Synchronous ===")
    run_sync()
    
    print("\n=== Asynchronous ===")
    asyncio.run(run_async())
    
    # Expected output:
    # === Synchronous ===
    # A: Starting
    # A: Done
    # B: Starting
    # B: Done
    # C: Starting
    # C: Done
    # Sync total: 3.0s
    #
    # === Asynchronous ===
    # A: Starting
    # B: Starting
    # C: Starting
    # A: Done
    # B: Done
    # C: Done
    # Async total: 1.0s
