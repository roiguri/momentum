# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Momentum** is a personal wellness coach built with Google's Agent Development Kit (ADK). The project uses a **phased, incremental development approach** with 11 distinct phases, each delivering a working, demo-able feature set. The final architecture is a **hub-and-spoke multi-agent system** with centralized long-term memory (Firestore).

### Competition Context

This is a **Kaggle Capstone Project** for the 5-Day AI Agents Intensive Course (Nov 10-14, 2025).

- **Track**: Concierge Agents (personal wellness use case)
- **Deadline**: December 1, 2025, 11:59 AM PT
- **Goal**: Demonstrate 3+ key course concepts, achieve high technical implementation score
- **Deliverables**: GitHub repo (public), writeup (<1500 words), optional video (<3min)

**Key Requirements**:
- Must demonstrate **at least 3** course concepts (we're targeting 8+)
- Code must have pertinent comments for implementation/design
- README.md with problem, solution, architecture, setup instructions
- NO API keys or passwords in code
- Optional: YouTube video demo for 10 bonus points

## Development Workflow

### Phase-Based Development Process

This project follows a strict phase-based workflow:

1. **Plan Phase**: Review `docs/phases/phase-{N}.md` for detailed implementation tasks
2. **Approve Plan**: Get user approval before starting implementation
3. **Implement**: Execute tasks following the phase plan
4. **Test**: Create/update evaluation set in `evals/evalset_phase{N}.json`
5. **Demo**: Verify feature works end-to-end
6. **Complete**: Update `docs/PROGRESS.md` with results
7. **Review**: Document learnings and adjust future phases if needed

### Critical Files to Update

- **`docs/PROGRESS.md`**: Update after each task and phase completion. This is the memory/tracking file.
- **`docs/roadmap.md`**: Update if architectural decisions change during implementation
- **Phase Files**: Create/update `docs/phases/phase-{N}.md` before starting each phase

### Before Any Implementation

1. Check `docs/PROGRESS.md` for current phase and status
2. Read the relevant phase file in `docs/phases/`
3. Get explicit approval from user before proceeding with implementation
4. Update PROGRESS.md as you complete tasks

### Documentation Guidelines

**For Tasks You Cannot Do** (Firebase setup, API keys, deployments):
- Provide explicit step-by-step user instructions in the phase file
- Document in README.md for project reproducibility
- Create `.env.example` templates with required variables
- Document all external service accounts and configurations

**Reference Documentation Usage**:
- Use Table of Contents in `docs/best-practices/best-practices.md` to navigate
- Read ONLY the relevant sections (don't parse entire document)
- This preserves token budget and improves efficiency

### After Completing Work

1. Update `docs/PROGRESS.md` with completion status
2. Get user approval that phase is complete before moving to next phase
3. Commit changes with descriptive message

## Project Architecture

### Hub-and-Spoke Pattern

- **Hub**: `WellnessChiefAgent` - Main orchestrator using LLM-based orchestration
- **Spokes**: Specialized agents (InstructorAgent, SchedulerAgent, TrackerAgent, etc.)
- **Memory**: Firestore for long-term memory across conversations
- **Sessions**:
  - Phases 1-3: `InMemorySessionService`
  - Phase 4+: `DatabaseSessionService` (required for Long-Running Operations)

### Key Architectural Principles

1. **MVA First**: Phase 1 creates Minimum Viable Agent with no external dependencies
2. **Incremental Complexity**: Each phase adds ONE new major capability
3. **Evaluation-Driven**: Every phase has its own eval set to prevent regressions
4. **Session Migration**: Explicit migration from InMemory to Database in Phase 4

## Common Commands

### Development

```bash
# Start ADK web interface with debug logging
adk web --log_level DEBUG

# Run agent in development mode
python main.py

# Run evaluations
adk eval run evals/evalset_phase1.json

# Run specific eval with config
adk eval agent_dir evalset.json --config_file_path=test_config.json
```

### Testing

```bash
# Test individual agent
adk web --log_level DEBUG

# Run all evals for regression testing
adk eval run evals/evalset_phase*.json
```

## ADK Best Practices (Key Points)

Refer to `docs/best-practices/` for comprehensive guidelines. Key principles:

### Agent Design

- **Specialize**: Each agent has ONE clear responsibility
- **Clear Instructions**: Specific, actionable instructions with expected behavior
- **State Management**: Use `output_key` and `{placeholders}` for state passing
- **Tool References**: Reference tools by exact function names in instructions

### Workflow Patterns

- **Sequential**: When order matters (use `SequentialAgent`)
- **Parallel**: When tasks are independent (use `ParallelAgent`)
- **Loop**: When iterative refinement needed (use `LoopAgent` with exit conditions)
- **LLM Orchestration**: When dynamic decisions needed (use `AgentTool`)

### Tool Integration

- **Function Tools**: Custom Python functions with clear docstrings and type hints
- **Agent Tools**: Wrap agents with `AgentTool` for delegation
- **MCP Tools**: External services (Google Calendar, Strava, etc.)
- **Code Execution**: Use `BuiltInCodeExecutor` for reliable calculations
- **LROs**: Use `ToolContext.request_confirmation()` for human-in-the-loop approvals

### Session Management

- **InMemorySessionService**: Development/testing (Phases 1-3)
- **DatabaseSessionService**: Production with persistence (Phase 4+, required for LROs)
- **Session State**: Use `tool_context.state` for conversation-scoped data

### Memory Management

- **Session vs Memory**: Sessions are temporary (one conversation), Memory is long-term (cross-conversation)
- **Transfer**: Explicitly call `memory_service.add_session_to_memory(session)`
- **Retrieval**: Agent needs `load_memory` or `preload_memory` tools to access memories

### Evaluation

- Create eval sets in `evals/evalset_phase{N}.json`
- Run evals after every change to prevent regressions
- Track evaluation scores in `docs/PROGRESS.md`

## Database Schema (Firestore)

Schema designed from Day 1 to support multiple goals:

- **users**: `active_goal_id`, `preferences`, `progression_modifiers`
- **goals**: `user_id`, `parent_goal_id`, `type`, `target_metric`, `target_value`, `is_active`
- **plan**: `user_id`, `goal_id`, `date`, `status`, `exercises[]`
- **workout_log**: `user_id`, `goal_id`, `plan_id`, `results`, `feedback`
- **nutrition_log**: `user_id`, `goal_id`, `meal_type`, `items_raw[]`, `macros_total`

All collections include `goal_id` field to support future multi-goal feature without refactoring.

## Phase Progression

| Phase | Name | Key Feature | Session Type |
|-------|------|-------------|--------------|
| 0 | Project Setup | Documentation & structure | N/A |
| 1 | Chat-Planner (MVA) | Conversational plan generation | InMemory |
| 2 | Instructor | Exercise explanations + Google Search | InMemory |
| 3 | Plan Persister | Save plans to Firestore | InMemory |
| 4 | Scheduler | Google Calendar + LRO | **Database** (migration) |
| 5 | Logger | Workout/adherence tracking | Database |
| 6 | Editor | Plan modification | Database |
| 7 | Nutritionist | Nutrition logging + Nutritionix API | Database |
| 8 | Adaptive Coach | Feedback loop + ParallelAgent | Database |
| 9 | Refiner | Safety critic LoopAgent | Database |
| 10 | A2A Service | Agent2Agent protocol | Database |
| 11 | Extensions | Strava integration + deployment | Database |

## Important Notes

- **Never skip phase approval**: Always get user approval before implementing
- **Always update PROGRESS.md**: This is the project memory file
- **Session migration is critical**: Phase 4 MUST migrate from InMemory to Database before implementing LROs
- **Eval sets are mandatory**: Every phase requires evaluation to prevent regressions
- **Follow the roadmap**: Phases build on each other; don't skip ahead

## Reference Documentation

- **Roadmap**: `docs/roadmap.md` - High-level architecture and all phases
- **Progress**: `docs/PROGRESS.md` - Current status, decisions, and tracking
- **Best Practices**: `docs/best-practices/best-practices.md` - Comprehensive ADK guidelines
- **Checklist**: `docs/best-practices/agents-checklist.md` - Development checklist
- **Phase Details**: `docs/phases/phase-{N}.md` - Detailed implementation plans
