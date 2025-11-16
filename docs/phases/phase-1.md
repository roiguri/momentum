# Phase 1: The "Chat-Planner" (The MVA)

**Status**: ⚪ Not Started
**Priority**: P0 (Foundational)
**Estimated Effort**: 2-3 hours

---

## Overview

**Goal**: Build a working, conversational agent that asks the user for their goals and generates a text-based workout plan.

**Demo**: User says, "Plan my 5k." The agent asks clarifying questions (e.g., "How many days a week can you train?") and then prints a structured, multi-week plan directly in the chat.

**Key Concepts**:
- Agent Design
- LLM-based Orchestration
- Session State (for preferences)
- `InMemorySessionService`

---

## Prerequisites

### Environment Setup (User Action Required)

**Python Environment**:
1. Install Python 3.10 or higher
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install google-adk
   ```

**API Keys Configuration** (User Action Required):
1. Get a Gemini API key:
   - Go to [Google AI Studio](https://aistudio.google.com/apikey)
   - Click "Create API Key"
   - Copy the key

2. Create `.env.local` file in project root:
   ```bash
   # .env.local (DO NOT COMMIT THIS FILE)
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. The `.env.local` file is gitignored for security

**Verification**:
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Virtual environment activated
- [ ] Google ADK installed (`pip show google-adk`)
- [ ] `.env.local` file created with valid API key

---

## Implementation Tasks

### Task 1: Project Setup
**Estimated Time**: 15 minutes

- [ ] Create `requirements.txt` with dependencies
- [ ] Create `.env` file for API keys (template only, actual keys in `.env.local`)
- [ ] Create `main.py` as entry point
- [ ] Test ADK installation with simple hello-world agent

**Acceptance Criteria**:
- `adk web` command runs successfully
- Can see basic agent interface in browser

---

### Task 2: Create WellnessChiefAgent (Hub)
**Estimated Time**: 45 minutes

- [ ] Create `agents/` directory structure
- [ ] Create `agents/hub.py` with `WellnessChiefAgent` class
- [ ] Write detailed instruction prompt for the agent:
  - Act as expert wellness coach
  - Ask for key preferences (goal type, days per week, experience level)
  - Generate general text-based plan based on preferences
- [ ] Configure agent with appropriate model (Gemini 1.5 Flash recommended for MVP)
- [ ] Use `InMemorySessionService` for session management

**Acceptance Criteria**:
- Agent responds conversationally
- Agent asks appropriate questions before generating plan
- Agent generates a reasonable multi-week plan structure

**Reference**: See `docs/best-practices/agent-design.md` for agent instruction patterns

---

### Task 3: Implement Session State Management
**Estimated Time**: 30 minutes

- [ ] Use `tool_context.state` to store user preferences during conversation
- [ ] Store: goal type, days_per_week, experience_level, current_week
- [ ] Agent retrieves state to maintain context across conversation turns

**Acceptance Criteria**:
- Agent remembers user preferences within a conversation
- Agent doesn't ask repeated questions
- State persists across multiple turns in same session

---

### Task 4: Plan Generation Logic
**Estimated Time**: 45 minutes

- [ ] Implement prompt engineering for plan generation
- [ ] Create structured plan format:
  ```
  Week 1:
    Day 1: [Exercise type] - [Details]
    Day 2: [Rest or active recovery]
    ...
  ```
- [ ] Support at least 2 goal types: "5k run" and "strength training"
- [ ] Generate 4-week initial plan

**Acceptance Criteria**:
- Plan is structured and readable
- Plan is appropriate for stated goal
- Plan includes rest days
- Plan shows progressive overload (gets harder over weeks)

---

### Task 5: Testing & Evaluation
**Estimated Time**: 45 minutes

- [ ] Create `evals/` directory
- [ ] Create `evals/evalset_phase1.json` with test cases:
  - Test: Agent asks for preferences
  - Test: Agent generates 5k plan
  - Test: Agent generates strength plan
  - Test: Agent handles unclear input gracefully
- [ ] Run evaluations: `adk eval run`
- [ ] Document results and any needed improvements

**Acceptance Criteria**:
- All eval test cases pass
- Agent behavior is consistent across runs
- Edge cases are handled gracefully

**Reference**: See `docs/best-practices/evaluation.md` for eval best practices

---

## Code Structure

After Phase 1, the repository should look like:

```
momentum/
├── agents/
│   ├── __init__.py
│   └── hub.py              # WellnessChiefAgent
├── evals/
│   └── evalset_phase1.json
├── main.py                 # Entry point
├── requirements.txt
├── .env.example            # Template
└── .env.local             # (gitignored) Actual keys
```

---

## Success Metrics

- [ ] Agent successfully engages in conversation
- [ ] Agent asks 2-3 relevant questions before generating plan
- [ ] Agent generates appropriate 4-week plan for stated goal
- [ ] Evaluation set passes with >80% success rate
- [ ] Demo-able: Can show working conversation → plan generation flow

---

## Implementation Notes

### Agent Instruction Template

```python
WELLNESS_CHIEF_INSTRUCTION = """
You are an expert wellness coach with deep knowledge of fitness, training, and
exercise science. Your role is to help users achieve their fitness goals through
personalized workout planning.

When a user requests a workout plan:
1. First, ask clarifying questions to understand:
   - Their specific goal (e.g., "run a 5k", "build strength", "lose weight")
   - How many days per week they can train
   - Their experience level (beginner, intermediate, advanced)
   - Any injuries or limitations

2. Once you have this information, generate a structured 4-week workout plan that:
   - Is appropriate for their experience level
   - Fits their available training days
   - Shows progressive overload (gradually increasing difficulty)
   - Includes rest/recovery days
   - Is specific to their goal

3. Present the plan in a clear, week-by-week format with specific exercises,
   sets, reps, or distances/times as appropriate.

Be encouraging, professional, and safety-conscious in all recommendations.
"""
```

### Session State Schema

```python
{
    "goal": str,              # e.g., "5k run", "strength training"
    "days_per_week": int,     # e.g., 3, 4, 5
    "experience_level": str,  # "beginner", "intermediate", "advanced"
    "plan_generated": bool    # Track if plan was created
}
```

---

## Potential Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Agent generates inconsistent plans | Strengthen instruction prompt with examples |
| Agent doesn't ask questions | Add explicit instruction to gather info first |
| Plans are too generic | Add more detail to prompt about progressive overload |
| Eval tests are flaky | Use more specific expected outputs in eval set |

---

## Next Phase Preview

**Phase 2** will add the `InstructorAgent` to explain how to perform exercises, using Google Search as a tool. This phase establishes the foundation that Phase 2 will build upon.

---

## Approval Checklist

**Before Implementation**:
- [ ] Phase plan reviewed and approved
- [ ] Prerequisites met
- [ ] Time estimate acceptable

**After Implementation**:
- [ ] All tasks completed
- [ ] Success metrics met
- [ ] Demo prepared and working
- [ ] PROGRESS.md updated
- [ ] Ready to commit and move to Phase 2
