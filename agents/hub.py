"""
WellnessChiefAgent - Main hub for personalized workout planning

Phase 1: Conversational plan generation with no external tools
Phase 2+: Will add InstructorAgent, Firestore tools, SchedulerAgent, etc.

Key Responsibilities:
- Gather user preferences (goal, training frequency, experience level)
- Generate structured, progressive 4-week workout plans
- Provide encouraging, professional coaching guidance

Architecture: LLM-based Orchestration (will add Agent Tools in later phases)
Session Management: InMemorySessionService (will migrate to Database in Phase 4)
"""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from .prompts import WELLNESS_CHIEF_PROMPT


def create_wellness_chief_agent() -> LlmAgent:
    return LlmAgent(
        name="WellnessChiefAgent",
        description="Main wellness coaching agent that creates personalized workout plans",
        model=Gemini(model="gemini-2.5-flash"),
        instruction=WELLNESS_CHIEF_PROMPT,
        tools=[],
    )
