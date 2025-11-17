"""
Root agent configuration for ADK web interface.

This file is required by the ADK web command structure.
It exports the root_agent instance that ADK discovers and runs.
"""

from .hub import create_wellness_chief_agent

root_agent = create_wellness_chief_agent()
