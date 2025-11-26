"""
Plan storage tools for workout plan persistence.

Uses Firestore-compatible JSON schema for seamless Phase 5-7 migration.
File-based storage in data/plans/{user_id}/ directory.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from google.adk.tools import FunctionTool


def save_plan(
    goal_description: str,
    exercises: str,
    week_number: int = 1,
    program_length_weeks: int = 4,
    notes: str = ""
) -> str:
    """
    Save a workout plan to persistent storage.
    
    Args:
        goal_description: User's fitness goal (e.g., "5k training", "strength building")
        exercises: Complete workout plan as formatted text
        week_number: Current week in the program (default: 1)
        program_length_weeks: Total program length in weeks (default: 4)
        notes: Additional notes about the plan
    
    Returns:
        plan_id: Unique identifier for the saved plan
    """
    user_id = "user"
    goal_id = goal_description.lower().replace(" ", "_")[:30]
    timestamp = datetime.now().isoformat()
    
    plan_data = {
        "user_id": user_id,
        "goal_id": goal_id,
        "created_at": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "proposed",
        "exercises_text": exercises,
        "metadata": {
            "week_number": week_number,
            "program_length_weeks": program_length_weeks,
            "notes": notes,
            "goal_description": goal_description
        }
    }
    
    plan_id = f"{goal_id}_week{week_number}"
    path = Path(f"data/plans/{user_id}/{plan_id}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(plan_data, f, indent=2)
    
    return f"Plan saved successfully with ID: {plan_id}"


def load_plan(plan_id: Optional[str] = None) -> str:
    """
    Load a saved workout plan.
    
    Args:
        plan_id: Specific plan ID to load. If not provided, loads the most recent plan.
    
    Returns:
        Plan details as formatted text
    """
    user_id = "user"
    plans_dir = Path(f"data/plans/{user_id}")
    
    if not plans_dir.exists():
        return "No saved plans found. Generate a plan first and ask me to save it."
    
    if plan_id:
        plan_path = plans_dir / f"{plan_id}.json"
        if not plan_path.exists():
            return f"Plan '{plan_id}' not found. Use list_user_plans to see available plans."
    else:
        plan_files = sorted(plans_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not plan_files:
            return "No saved plans found."
        plan_path = plan_files[0]
    
    with open(plan_path, 'r') as f:
        plan_data = json.load(f)
    
    metadata = plan_data.get("metadata", {})
    result = f"""**Workout Plan: {metadata.get('goal_description', 'Unknown Goal')}**

Created: {plan_data.get('created_at', 'Unknown')}
Status: {plan_data.get('status', 'Unknown')}
Week: {metadata.get('week_number', '?')} of {metadata.get('program_length_weeks', '?')}

{plan_data.get('exercises_text', 'No exercises found')}

Notes: {metadata.get('notes', 'None')}
"""
    return result


def get_current_week_plan(week_number: Optional[int] = None) -> str:
    """
    Get the workout plan for a specific week.
    
    Args:
        week_number: Week number to retrieve. If not provided, returns week 1.
    
    Returns:
        Week's workout plan as formatted text
    """
    user_id = "user"
    plans_dir = Path(f"data/plans/{user_id}")
    
    if not plans_dir.exists():
        return "No saved plans found. Generate a plan first and ask me to save it."
    
    if week_number is None:
        week_number = 1
    
    plan_files = list(plans_dir.glob(f"*_week{week_number}.json"))
    
    if not plan_files:
        return f"No plan found for week {week_number}. Available weeks can be found using list_user_plans."
    
    with open(plan_files[0], 'r') as f:
        plan_data = json.load(f)
    
    metadata = plan_data.get("metadata", {})
    result = f"""**Week {week_number} Workout Plan**

Goal: {metadata.get('goal_description', 'Unknown')}

{plan_data.get('exercises_text', 'No exercises found')}
"""
    return result


def list_user_plans() -> str:
    """
    List all saved workout plans for the current user.
    
    Returns:
        Formatted list of all saved plans
    """
    user_id = "user"
    plans_dir = Path(f"data/plans/{user_id}")
    
    if not plans_dir.exists() or not list(plans_dir.glob("*.json")):
        return "No saved plans found. Generate a plan and ask me to save it."
    
    plan_files = sorted(plans_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    result = "**Your Saved Workout Plans:**\n\n"
    for plan_file in plan_files:
        with open(plan_file, 'r') as f:
            plan_data = json.load(f)
        
        metadata = plan_data.get("metadata", {})
        plan_id = plan_file.stem
        result += f"- **{plan_id}**: {metadata.get('goal_description', 'Unknown Goal')} "
        result += f"(Week {metadata.get('week_number', '?')}/{metadata.get('program_length_weeks', '?')}, "
        result += f"Status: {plan_data.get('status', 'Unknown')})\n"
    
    return result


save_plan_tool = FunctionTool(func=save_plan)
load_plan_tool = FunctionTool(func=load_plan)
get_current_week_plan_tool = FunctionTool(func=get_current_week_plan)
list_user_plans_tool = FunctionTool(func=list_user_plans)
