"""
Root agent configuration for ADK web interface.

This file is required by the ADK web command structure.
It exports the root_agent instance that ADK discovers and runs.
"""

from pathlib import Path
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from momentum_agent.hub import create_wellness_chief_agent

load_dotenv()

# Get absolute path to project root and ensure data directory exists
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "wellness_sessions.db"

root_agent = create_wellness_chief_agent()

session_service = DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{DB_PATH}")
memory_service = InMemoryMemoryService()

runner = Runner(
    agent=root_agent,
    app_name="momentum",
    session_service=session_service,
    memory_service=memory_service
)

# Alias for AgentEvaluator compatibility
agent = root_agent
