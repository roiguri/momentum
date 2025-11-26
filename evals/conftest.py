"""
Pytest configuration for agent evaluations.

This module provides fixtures to ensure proper cleanup of async resources,
particularly aiohttp sessions used by google-genai, to prevent resource leaks
and ensure test isolation.
"""

import asyncio
import gc
import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def cleanup_aiohttp_sessions():
    """
    Automatically clean up aiohttp sessions after each test.
    
    This fixture runs after every test to ensure that any aiohttp.ClientSession
    objects created by google-genai are properly closed, preventing:
    - Resource leaks (file descriptors, memory)
    - Connection pool pollution between tests
    - Non-deterministic test failures due to stale connections
    """
    # Run the test
    yield
    
    # Force garbage collection to identify unclosed sessions
    gc.collect()
    
    # Close any remaining aiohttp sessions
    try:
        # Import here to avoid dependency if aiohttp isn't installed
        import aiohttp
        
        # Find and close all open ClientSession objects
        loop = asyncio.get_event_loop()
        for obj in gc.get_objects():
            if isinstance(obj, aiohttp.ClientSession):
                if not obj.closed:
                    loop.run_until_complete(obj.close())
    except ImportError:
        # aiohttp not installed, nothing to clean up
        pass
    except RuntimeError:
        # No event loop available, sessions will be cleaned up by garbage collector
        pass

