"""
InstructorAgent - Specialized agent for exercise instruction and form guidance.

Provides step-by-step exercise instructions with video resources using Google Search.
Maintains session context to provide concise answers first, detailed follow-ups when asked.
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
    
    Maintains session context automatically (inherited from parent Runner)
    to remember previous exercise discussions, enabling concise first 
    responses and detailed follow-ups.
    """
    return LlmAgent(
        name="InstructorAgent",
        description="Provides exercise instruction with proper form and YouTube video demonstrations. Uses a two-tier approach: concise overview on first mention, detailed breakdown for follow-up questions. Call this agent when users ask how to perform an exercise. Pass the user's question as the 'request' parameter.",
        model=Gemini(model="gemini-2.5-flash", retry_options=RETRY_CONFIG),
        instruction=INSTRUCTOR_PROMPT,
        tools=[google_search],
        output_key="exercise_instructions",
    )
