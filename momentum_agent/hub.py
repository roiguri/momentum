"""
WellnessChiefAgent - Main hub for personalized workout planning

Phase 1: Conversational plan generation with no external tools
Phase 2: Added InstructorAgent for exercise instruction
Phase 3+: Will add Firestore tools, SchedulerAgent, etc.

Key Responsibilities:
- Gather user preferences (goal, training frequency, experience level)
- Generate structured, progressive workout plans
- Delegate exercise instruction questions to InstructorAgent
- Provide encouraging, professional coaching guidance

Architecture: Hub-and-Spoke with Agent Tools
Session Management: InMemorySessionService (will migrate to Database in Phase 4)
"""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import AgentTool, preload_memory
from .prompts import WELLNESS_CHIEF_PROMPT
from .config import RETRY_CONFIG
from .spokes.instructor import create_instructor_agent
from .tools.plan_tools import (
    save_plan_tool,
    load_plan_tool,
    get_current_week_plan_tool,
    list_user_plans_tool
)


async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


def create_wellness_chief_agent() -> LlmAgent:
    instructor_agent = create_instructor_agent()

    return LlmAgent(
        name="WellnessChiefAgent",
        description="Main wellness coaching agent that creates personalized workout plans and provides exercise instruction",
        model=Gemini(model="gemini-2.5-flash", retry_options=RETRY_CONFIG),
        instruction=WELLNESS_CHIEF_PROMPT,
        tools=[
            AgentTool(agent=instructor_agent),
            preload_memory,
            save_plan_tool,
            load_plan_tool,
            get_current_week_plan_tool,
            list_user_plans_tool,
        ],
        after_agent_callback=auto_save_to_memory,
    )
