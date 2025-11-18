# Phase 2: The "Instructor" (Adding a Spoke)

**Status**: ✅ Completed
**Priority**: P1 (Core Feature)
**Actual Effort**: 4 hours
**Completed**: 2025-11-18

---

## Overview

**Goal**: Add the InstructorAgent to explain exercises and provide instructional resources.

**Demo**: User asks, "How do I do a proper squat?" The agent provides a step-by-step text explanation and uses Google Search to find relevant YouTube video links.

**Key Concepts**:
- Agent Specialization (spoke agents)
- Agent Tools (using one agent as a tool for another)
- Built-in Tools (Google Search)
- Callbacks and Plugins (observability)
- Agent Evaluation (web UI exports)

---

## Prerequisites

### Environment (Already Complete from Phase 1)
- [x] Python 3.10+ installed
- [x] Virtual environment activated
- [x] Google ADK with eval module installed
- [x] `.env.local` file with GOOGLE_API_KEY

### New Requirements
- [ ] Review Google Search tool documentation in best practices
- [ ] Understand Agent Tools pattern from best practices
- [ ] Familiarize with LoggingPlugin implementation

---

## Implementation Tasks

### Task 1: Create InstructorAgent ✅
**Actual Time**: 90 minutes

- [x] Create `agents/spokes/` directory
- [x] Create `agents/spokes/__init__.py`
- [x] Create `agents/spokes/instructor.py` with `create_instructor_agent()` function
- [x] Create instruction prompt in `agents/prompts/instructor.py`:
  - Specialized in exercise instruction
  - Uses Google Search to find YouTube videos
  - Provides step-by-step safety-focused guidance
  - Returns structured response with both text instructions and video links
  - Added flexibility for video count based on exercise complexity
  - Fixed double-response issue with single comprehensive response pattern
- [x] Configure agent with Google Search built-in tool
- [x] Added `output_key="exercise_instructions"` for explicit state tracking
- [x] Test InstructorAgent standalone via `adk web`

**Acceptance Criteria**:
- ✅ InstructorAgent responds to exercise questions
- ✅ Agent uses Google Search to find relevant YouTube videos
- ✅ Provides safe, step-by-step exercise instructions
- ✅ Response includes appropriate number of high-quality instructional video links
- ✅ Single comprehensive response (no partial/double responses)

**Reference**: `docs/best-practices/best-practices.md` - Tool Integration section

---

### Task 2: Integrate InstructorAgent into WellnessChiefAgent ✅
**Actual Time**: 120 minutes (including debugging)

- [x] Update `agents/hub.py` to import and use InstructorAgent as an Agent Tool
- [x] Update WellnessChiefAgent instruction prompt to:
  - Recognize exercise instruction requests
  - Delegate to InstructorAgent when user asks "how to" questions
  - Maintain conversation flow after receiving instruction responses
  - **Critical fix**: Added explicit instructions to present complete tool response
  - Added "Do NOT stop after calling the tool" guidance
- [x] Test integration via `adk web`
- [x] Verify hub correctly routes exercise questions to InstructorAgent
- [x] Debug and fix empty response issue with AgentTool
- [x] Research and apply best practices from Kaggle ADK notebooks

**Acceptance Criteria**:
- ✅ WellnessChiefAgent recognizes exercise instruction requests
- ✅ Delegates to InstructorAgent using Agent Tool pattern
- ✅ Returns InstructorAgent responses to user seamlessly
- ✅ Can handle both plan generation and exercise instruction in same conversation
- ✅ Tool responses flow back correctly (no empty responses)

**Key Learnings**:
- LLM-based orchestration requires extremely explicit prompts about tool response handling
- `output_key` parameter aids debugging and makes state flow explicit
- Critical prompt pattern: "Call tool → receive response → present COMPLETE response to user"

**Reference**: `docs/best-practices/best-practices.md` - Agent Tools section

---

### Task 3: Implement Observability with LoggingPlugin
**Status**: ⏳ In Progress (to be completed after this commit)
**Estimated Time**: 45 minutes

- [ ] Create `core/` directory
- [ ] Create `core/observability.py` with LoggingPlugin implementation
- [ ] Implement callbacks for:
  - `before_agent`: Log agent invocations
  - `after_agent`: Log agent completions and outputs
  - `before_tool`: Log tool usage
  - `after_tool`: Log tool results
- [ ] Create basic logging configuration
- [ ] Test logging output during agent interactions

**Note**: Will implement this next, after committing core multi-agent functionality.

---

### Task 4: Evaluation Setup
**Status**: ⏳ Pending (to be completed after observability)
**Estimated Time**: 60 minutes

- [x] Manual testing via `adk web` (completed informally)
- [ ] Create `evals/` directory
- [ ] Use `adk web` to export successful test conversations
- [ ] Create `evals/evalset_phase1_phase2.json` with test cases
- [ ] Create/update `evals/test_config.json` with eval criteria
- [ ] Run initial evaluation and document baseline scores

**Note**: Manual testing confirmed both Phase 1 and Phase 2 functionality work correctly. Will establish formal evaluation workflow next.

---

### Task 5: Documentation and Testing ✅
**Actual Time**: 30 minutes

- [x] Update `docs/phases/phase-2.md` with completion status
- [x] Document key learnings from AgentTool debugging
- [x] Test full workflow manually:
  - User requests workout plan ✅
  - Agent generates plan ✅
  - User asks how to perform specific exercise ✅
  - Agent provides instructions with video links ✅
- [x] Document prompt refinements and debugging insights

**Acceptance Criteria**:
- ✅ All documentation up to date
- ✅ Phase 2 demo-able end-to-end
- ✅ Key learnings documented for future reference
- ✅ Ready for commit and Phase 3 planning

---

## Code Structure

After Phase 2, the repository should look like:

```
momentum/
├── agents/
│   ├── __init__.py
│   ├── agent.py            # Root agent export
│   ├── hub.py              # WellnessChiefAgent (updated with InstructorAgent tool)
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── wellness_chief.py
│   │   └── instructor.py   # NEW
│   ├── spokes/
│   │   ├── __init__.py     # NEW
│   │   └── instructor.py   # NEW - InstructorAgent
│   └── .env
├── core/
│   ├── __init__.py         # NEW
│   └── observability.py    # NEW - LoggingPlugin
├── docs/
│   ├── roadmap.md
│   ├── PROGRESS.md
│   ├── prompt-engineering.md
│   └── phases/
│       ├── phase-1.md
│       └── phase-2.md      # NEW
├── evals/
│   ├── evalset_phase1_phase2.json  # NEW
│   ├── test_config.json    # NEW
│   └── README.md           # NEW
├── requirements.txt
├── .env.example
└── .env.local
```

---

## Success Metrics

- [x] InstructorAgent provides accurate exercise instructions
- [x] Google Search integration finds relevant YouTube videos
- [x] WellnessChiefAgent correctly delegates to InstructorAgent
- [ ] LoggingPlugin captures all agent and tool interactions (In Progress)
- [ ] Evaluation workflow established with web UI exports (Pending)
- [ ] >80% evaluation pass rate for combined Phase 1 + Phase 2 tests (Pending)
- [x] Demo-able: Plan generation + exercise instruction in single conversation

**Phase 2 Core Multi-Agent Objectives: ✅ ACHIEVED**
**Remaining**: Observability & Evaluation (in progress)

---

## Prompt Engineering Notes

### InstructorAgent Instruction Template

**Key Requirements**:
- **Persona**: Expert personal trainer and exercise coach
- **Task**: Provide safe, clear exercise instructions with video resources
- **Context**: User may be beginner, intermediate, or advanced
- **Format**: Step-by-step text + 1-2 YouTube video links

**Safety Considerations**:
- Always emphasize proper form over weight/reps
- Warn about common mistakes
- Suggest modifications for beginners
- Note when professional supervision is recommended

**Example Prompt Structure**:
```
You are an expert personal trainer specializing in exercise instruction.
When asked about an exercise:
1. Provide step-by-step instructions emphasizing proper form
2. Use Google Search to find 1-2 high-quality YouTube instructional videos
3. Warn about common mistakes
4. Suggest modifications for different skill levels
```

---

## Testing Scenarios

### Scenario 1: Exercise Instruction Only
- User: "How do I do a squat?"
- Expected: Step-by-step instructions + YouTube links

### Scenario 2: Plan Then Instruction
- User: "Create a 4-week strength plan, 3 days/week, beginner"
- Agent: Generates plan
- User: "How do I do a deadlift?"
- Expected: Instructions + video links

### Scenario 3: Multiple Exercise Questions
- User asks about multiple exercises in succession
- Expected: Each gets proper instructions + videos

---

## Potential Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Google Search returns low-quality videos | Refine search queries in prompt, add quality filters |
| InstructorAgent not delegated correctly | Improve hub prompt to recognize instruction requests |
| Logging too verbose | Adjust LoggingPlugin to filter noise |
| Web UI export format unclear | Review ADK docs, start with simple exports |
| Evaluation scores too low | Adjust criteria, improve expected responses |

---

## Approval Checklist

**Before Implementation**:
- [ ] Phase 2 plan reviewed and approved
- [ ] Time estimate acceptable
- [ ] Prerequisites understood

**After Implementation**:
- [x] Core tasks completed (Tasks 1-2, Task 5)
- [x] Success metrics met (core objectives)
- [x] Demo prepared and working
- [ ] PROGRESS.md updated (will update before commit)
- [ ] Evaluations passing (Deferred to Phase 3)
- [x] Ready to commit and move to Phase 3

---

## Lessons Learned & Debugging Insights

### Critical Discovery: LLM Orchestration Requires Explicit Flow Instructions

**Problem Encountered**: When WellnessChiefAgent called InstructorAgent via AgentTool, it would stop execution and return empty response after the tool call.

**Root Cause**: The LLM didn't understand it needed to:
1. Call the tool
2. Wait for response
3. **Present the response to the user**

**Solution**: Extremely explicit prompt instructions:
```markdown
**IMPORTANT:** When a user asks how to perform an exercise:
1. Call the InstructorAgent tool immediately
2. After the tool completes, you will receive its full response
3. Present the COMPLETE response from the InstructorAgent to the user
4. Do NOT stop after calling the tool - you MUST relay the full instructions
```

### Key Technical Insights

1. **`output_key` Parameter**
   - While not strictly required for AgentTool response flow, it makes state management explicit
   - Invaluable for debugging (can see what's stored where)
   - Self-documenting code benefit
   - **Recommendation**: Always use `output_key` on agents in multi-agent systems

2. **AgentTool vs Sub-Agents**
   - `AgentTool`: For delegation where response returns to caller (what we used)
   - `SequentialAgent/ParallelAgent/LoopAgent`: For deterministic workflows
   - LLM-based orchestration is powerful but "unpredictable" (per Kaggle notebooks)
   - Consider Sequential patterns for production-critical flows

3. **InMemoryRunner for Testing**
   - Much simpler API than manual Runner setup
   - Automatically creates in-memory services
   - Has convenient `run_debug()` method
   - Matches pattern from official Kaggle notebooks

4. **Prompt Engineering Pattern for Tool Usage**
   ```
   ## Available Tools
   You have access to [ToolName] for [purpose].

   **IMPORTANT:** When [condition]:
   1. Call the tool
   2. After tool completes, you will receive its response
   3. Present the COMPLETE response to user
   4. Do NOT stop after calling the tool
   ```

### What Worked Well

- ✅ Creating InstructorAgent as isolated, testable component
- ✅ Testing standalone before integration
- ✅ Using ADK web UI for rapid iteration
- ✅ Researching Kaggle notebooks for best practices
- ✅ Systematic debugging with inspection scripts

### What Could Be Improved

- ⚠️ Initial underestimation of multi-agent orchestration complexity
- ⚠️ Should have researched AgentTool patterns before implementation
- ⚠️ Deferred observability/evaluation - should prioritize earlier in Phase 3

### Recommendations for Future Phases

1. **Always test agents standalone first** before integration
2. **Be extremely explicit in orchestration prompts** - LLMs need step-by-step flow guidance
3. **Use `output_key`** consistently for better debugging
4. **Consider Sequential patterns** for critical production flows vs LLM orchestration
5. **Implement logging early** - would have accelerated debugging
6. **Establish evaluation baseline** before making changes

---
