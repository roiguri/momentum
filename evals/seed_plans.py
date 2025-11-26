import json
from pathlib import Path
from momentum_agent.tools.plan_tools import save_plan
from datetime import datetime

def seed_plans():
    user_id = "user"
    # Ensure directory exists
    plans_dir = Path(f"data/plans/{user_id}")
    plans_dir.mkdir(parents=True, exist_ok=True)

    # Plan 1: 5k Run
    plan1_id = "run_a_5k_week1"
    plan1_data = {
        "user_id": user_id,
        "goal_id": "run_a_5k",
        "created_at": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
        "exercises_text": "Week 1:\nDay 1: 20 min run\nDay 2: Rest\nDay 3: 20 min run",
        "metadata": {
            "week_number": 1,
            "program_length_weeks": 8,
            "notes": "Focus on consistency",
            "goal_description": "Run a 5k"
        }
    }

    with open(plans_dir / f"{plan1_id}.json", "w") as f:
        json.dump(plan1_data, f, indent=2)
    
    save_plan(
        goal_description="Run a 5k",
        exercises="""**Week 2: Building Endurance**
Day 1: 25 min run
Day 2: Rest
Day 3: 25 min run
Day 4: Rest
Day 5: 30 min run
Day 6: Cross-training (30 min)
Day 7: Rest""",
        week_number=2,
        program_length_weeks=8,
        notes="Increase duration slightly."
    )
    
    print("Dummy plans created successfully.")

    # Plan 2: Strength
    plan2_id = "beginner_strength_week1"
    plan2_data = {
        "user_id": user_id,
        "goal_id": "beginner_strength",
        "created_at": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "completed",
        "exercises_text": "Week 1:\nDay 1: Full body\nDay 2: Rest\nDay 3: Full body",
        "metadata": {
            "week_number": 1,
            "program_length_weeks": 4,
            "notes": "Start light",
            "goal_description": "Beginner Strength"
        }
    }

    with open(plans_dir / f"{plan2_id}.json", "w") as f:
        json.dump(plan2_data, f, indent=2)

    print(f"Created {plan2_id}")

if __name__ == "__main__":
    seed_plans()
