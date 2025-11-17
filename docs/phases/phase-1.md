# Phase 1: The "Chat-Planner" (The MVA)

**Status**: 🟡 In Progress (Evaluation Pending)
**Priority**: P0 (Foundational)
**Estimated Effort**: 2-3 hours
**Actual Effort**: ~2.5 hours

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

### Task 1: Project Setup ✅
**Estimated Time**: 15 minutes
**Actual Time**: ~20 minutes

- [x] Create `requirements.txt` with dependencies
- [x] Create `.env.example` file for API keys (template only, actual keys in `.env.local`)
- [x] Create `agents/agent.py` as ADK entry point with `root_agent` export
- [x] Test ADK installation with agent structure

**Acceptance Criteria**:
- ✅ `adk web --log_level DEBUG` command runs successfully
- ✅ Can see basic agent interface in browser

**Notes**:
- ADK requires `agents/agent.py` with `root_agent` export, not standalone config file
- Created `.env` symlink in `agents/` directory for ADK auto-loading

---

### Task 2: Create WellnessChiefAgent (Hub) ✅
**Estimated Time**: 45 minutes
**Actual Time**: ~50 minutes

- [x] Create `agents/` directory structure
- [x] Create `agents/hub.py` with `create_wellness_chief_agent()` function
- [x] Write detailed instruction prompt for the agent:
  - Act as expert wellness coach
  - Ask for key preferences (goal type, days per week, experience level, timeline, limitations)
  - Generate personalized text-based plan based on preferences
- [x] Configure agent with appropriate model (using `gemini-2.5-flash` - latest stable)
- [x] Create `agents/prompts/` package with `wellness_chief.py` module

**Acceptance Criteria**:
- ✅ Agent responds conversationally
- ✅ Agent asks appropriate questions before generating plan
- ✅ Agent generates a reasonable multi-week plan structure with flexible timeline

**Notes**:
- Prompts structured as Python modules with PROMPT constant (cleaner than file I/O)
- Using Gemini 2.5 Flash instead of 1.5 Flash (latest stable model)
- Enhanced prompt to support variable-length programs (not just 4 weeks)
- Session management via InMemorySessionService (implicit in Phase 1, explicit in later phases)

---

### Task 3: Implement Session State Management ⚠️ DEFERRED
**Estimated Time**: 30 minutes
**Status**: Deferred to Future Phase

**Decision**: This task has been deferred to a later phase (Phase 3 or 4) for the following reasons:
- Gemini 2.5 Flash has 1M token context window, sufficient for Phase 1 conversation context
- Session state serves a **different purpose** from permanent memory (Firestore, Phase 3+)
- Session state = temporary conversation context within single session
- Permanent memory = historical data across sessions (user profile, past plans, progress)
- Will implement explicit session state when it adds value beyond LLM context

**Original Requirements** (to be revisited):
- [ ] Use `tool_context.state` to store user preferences during conversation
- [ ] Store: goal type, days_per_week, experience_level, timeline, current_week
- [ ] Agent retrieves state to maintain context across conversation turns

**Future Implementation Trigger**:
When implementing Firestore integration (Phase 3+), add session state management to track:
- Temporary conversation flow state
- Multi-turn interaction progress
- User preferences before permanent storage

**Note**: This is complementary to Memory Bank, not a replacement

---

### Task 4: Plan Generation Logic ✅
**Estimated Time**: 45 minutes
**Actual Time**: ~60 minutes (including timeline refinement)

- [x] Implement prompt engineering for plan generation using PTCF framework
- [x] Create structured plan format:
  ```
  Week 1:
    Day 1: [Exercise type] - [Specific details: sets x reps, distance, time]
    Day 2: [Rest or active recovery]
    ...
  Week N: [Progressive overload from previous weeks]
  ```
- [x] Support multiple goal types: "5k run", "strength training", "general fitness", "weight loss"
- [x] Generate variable-length plans based on user timeline (4 weeks, 8 weeks, or date-specific)
- [x] Create `docs/prompt-engineering.md` to track prompt refinements

**Acceptance Criteria**:
- ✅ Plan is structured and readable
- ✅ Plan is appropriate for stated goal
- ✅ Plan includes rest days
- ✅ Plan shows progressive overload (gets harder over weeks)
- ✅ Plan length matches user's timeline/goal date

**Key Refinements**:
- Removed hardcoded 4-week constraint
- Added timeline question (#3) in agent's information gathering
- Enhanced prompt with progression scaling guidance based on program length
- Documented prompt engineering best practices and resources

---

### Task 5: Testing & Evaluation ⏳
**Estimated Time**: 45 minutes
**Status**: In Progress

- [ ] Create `evals/` directory
- [ ] Create `evals/evalset_phase1.json` with test cases:
  - Test: Agent asks for preferences (goal, availability, timeline, experience)
  - Test: Agent generates 5k plan with appropriate progression
  - Test: Agent generates strength plan with appropriate progression
  - Test: Agent respects user's timeline (variable-length programs)
  - Test: Agent handles unclear input gracefully
  - Test: Agent includes safety considerations (rest days, 10% rule)
- [ ] Run evaluations: `adk eval run`
- [ ] Document results and any needed improvements

**Acceptance Criteria**:
- All eval test cases pass with >80% success rate
- Agent behavior is consistent across runs
- Edge cases are handled gracefully
- Variable timeline feature works correctly

**Reference**: See `docs/best-practices/evaluation.md` for eval best practices

**Next Steps**: Create evaluation set after documentation commit

---

## Code Structure

After Phase 1, the repository should look like:

```
momentum/
├── agents/
│   ├── __init__.py
│   ├── agent.py            # ADK entry point with root_agent export
│   ├── hub.py              # WellnessChiefAgent
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── wellness_chief.py  # PROMPT constant
│   └── .env               # Symlink to ../.env.local
├── docs/
│   ├── roadmap.md
│   ├── PROGRESS.md
│   ├── prompt-engineering.md
│   └── phases/
│       └── phase-1.md
├── evals/
│   └── evalset_phase1.json
├── requirements.txt
├── .env.example            # Template
└── .env.local             # (gitignored) Actual keys
```

---

## Success Metrics

- [x] Agent successfully engages in conversation
- [x] Agent asks 4-5 relevant questions before generating plan (goal, availability, timeline, experience, limitations)
- [x] Agent generates appropriate variable-length plan for stated goal and timeline
- [ ] Evaluation set passes with >80% success rate (pending eval creation)
- [x] Demo-able: Can show working conversation → plan generation flow
- [x] Prompt engineering best practices documented for future refinements

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
