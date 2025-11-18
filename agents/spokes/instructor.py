"""
InstructorAgent - Specialized agent for exercise instruction and form guidance.

Provides step-by-step exercise instructions with video resources using Google Search.
"""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import google_search
from ..prompts import INSTRUCTOR_PROMPT
from ..config import RETRY_CONFIG


def create_instructor_agent() -> LlmAgent:
    """
    Create the InstructorAgent specialized in exercise instruction.

    Uses Google Search to find high-quality YouTube instructional videos
    and provides safe, detailed guidance on proper exercise form.
    """
    return LlmAgent(
        name="InstructorAgent",
        description="Provides detailed exercise instruction with proper form, common mistakes, modifications, and YouTube video demonstrations. Call this agent when users ask how to perform an exercise. Pass the user's question as the 'request' parameter.",
        model=Gemini(model="gemini-2.5-flash", retry_options=RETRY_CONFIG),
        instruction=INSTRUCTOR_PROMPT,
        tools=[google_search],
        output_key="exercise_instructions",
    )
