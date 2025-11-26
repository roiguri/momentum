"""
Test evaluation for Momentum agent features using ADK's AgentEvaluator.

This uses the official ADK evaluation API following the standard format
from google/adk-samples.
"""

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import os


@pytest.mark.asyncio
async def test_instructor_agent():
    """Test InstructorAgent exercise instruction responses."""
    await AgentEvaluator.evaluate(
        "momentum_agent",
        os.path.join(os.path.dirname(__file__), "test_sets/instructor_agent.test.json"),
        num_runs=1,
    )


# TODO: Re-implement robust cross-session persistence tests when AgentEvaluator
# or a suitable framework supports memory service injection reliably.
# Current ADK evaluation environment has limitations with preload_memory tool dependency.

@pytest.mark.asyncio
async def test_user_memory():
    """Test user memory recall and preference tracking."""
    await AgentEvaluator.evaluate(
        "momentum_agent",
        os.path.join(os.path.dirname(__file__), "test_sets/user_memory.test.json"),
        num_runs=1,
    )


@pytest.mark.asyncio
async def test_plan_storage():
    """Test workout plan creation and storage."""
    await AgentEvaluator.evaluate(
        "momentum_agent",
        os.path.join(os.path.dirname(__file__), "test_sets/plan_storage.test.json"),
        num_runs=1,
    )
