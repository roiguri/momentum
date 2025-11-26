# Momentum - Development Progress Tracker

**Last Updated**: 2025-11-17

---

## Competition Context

**Event**: Kaggle 5-Day AI Agents Intensive Course Capstone Project
**Track**: Concierge Agents (agents useful for individuals in their own lives)
**Submission Deadline**: December 1, 2025, 11:59 AM PT
**Team**: Individual submission

### Submission Requirements Checklist

#### Category 1: The Pitch (30 points)
- [ ] **Core Concept & Value** (15 points): Clear problem statement, innovative solution, meaningful use of agents
- [ ] **Writeup** (15 points): Problem, solution, architecture, and project journey (<1500 words)

#### Category 2: The Implementation (70 points)
- [ ] **Technical Implementation** (50 points): Must include at least 3 key concepts from course:
  - [ ] Multi-agent system (Hub-and-Spoke with Sequential, Parallel, Loop agents)
  - [ ] Tools (MCP for Google Calendar/Strava, Custom tools, Code Execution, Google Search)
  - [ ] Long-Running Operations (LRO with user approval workflow)
  - [ ] Sessions & Memory (InMemory → Database migration, Memory Bank)
  - [ ] Context Engineering (context compaction)
  - [ ] Agent Evaluation (eval sets for each phase)
  - [ ] A2A Protocol (Phase 10)
  - [ ] Agent Deployment (Phase 11)
- [ ] **Documentation** (20 points): README.md with problem, solution, architecture, setup instructions, diagrams

#### Bonus Points (up to 20 points)
- [ ] **Effective Use of Gemini** (5 points): Gemini powers agents
- [ ] **Agent Deployment** (5 points): Deploy using Agent Engine or Cloud Run
- [ ] **YouTube Video** (10 points): <3 min video with problem, agents rationale, architecture, demo, build process

#### Submission Deliverables
- [ ] Title and subtitle
- [ ] Card/thumbnail image
- [ ] Track selection: Concierge Agents
- [ ] YouTube video URL (optional, for bonus points)
- [ ] Project description (<1500 words)
- [ ] GitHub repository (public) OR Kaggle notebook

### Key Concepts Coverage

This project demonstrates **8 of 11** key concepts from the course:

1. ✅ **Multi-agent system**: Hub (WellnessChiefAgent) + Spokes (Instructor, Scheduler, Tracker, Nutritionist, PlanGenerator)
2. ✅ **Sequential agents**: Plan generation pipeline
3. ✅ **Parallel agents**: Weekly summary aggregation (Phase 8)
4. ✅ **Loop agents**: Critic loop for safe progression (Phase 9)
5. ✅ **MCP Tools**: Google Calendar (Phase 4), Strava (Phase 11)
6. ✅ **Custom tools**: Firestore CRUD operations
7. ✅ **Built-in tools**: Google Search (Phase 2), Code Execution (Phase 7)
8. ✅ **Long-Running Operations**: User approval for calendar scheduling (Phase 4)
9. ✅ **Sessions & State**: InMemory → Database migration (Phase 4)
10. ✅ **Long-term Memory**: Firestore + Memory consolidation
11. ✅ **Context Engineering**: Context compaction configuration
12. ✅ **Observability**: `adk web --log_level DEBUG` throughout
13. ✅ **Agent Evaluation**: Eval sets for each phase
14. ✅ **A2A Protocol**: Agent exposed as A2A service (Phase 10)
15. ✅ **Agent Deployment**: Deploy to Agent Engine (Phase 11)

---

## Current Status

**Active Phase**: Phase 4 - Sessions, Memory & LROs (Combined) - Complete (Goals 1-3)
**Overall Progress**: 3/11 phases completed (27%)

---

## Phase Completion Tracking

| Phase | Name | Status | Started | Completed | Demo-able? |
|-------|------|--------|---------|-----------|------------|
| 0 | Project Setup | ✅ Complete | 2025-11-16 | 2025-11-16 | N/A |
| 1 | Chat-Planner (MVA) | ✅ Complete | 2025-11-16 | 2025-11-17 | ✅ Yes |
| 2 | Instructor (Adding a Spoke) | ✅ Complete | 2025-11-18 | 2025-11-18 | ✅ Yes |
| 3 | ~~Plan Persister~~ | ⚠️ **SKIPPED** | - | - | - |
| 4 | Sessions, Memory & LROs | 🔄 In Progress | 2025-11-23 | - | ✅ Partial |
| 5 | Logger (Detailed & Adherence) | ⚪ Not Started | - | - | - |
| 6 | Editor (Plan Modification) | ⚪ Not Started | - | - | - |
| 7 | Nutritionist (Core Feature) | ⚪ Not Started | - | - | - |
| 8 | Adaptive Coach (First Loop) | ⚪ Not Started | - | - | - |
| 9 | Refiner (Critic Loop) | ⚪ Not Started | - | - | - |
| 10 | A2A Service (Capstone) | ⚪ Not Started | - | - | - |
| 11 | Extensions & Polish | ⚪ Not Started | - | - | - |

---

## Phase 0: Project Setup ✅

**Goal**: Initialize repository structure, documentation, and development workflow

**Tasks**:
- [x] Initialize Git repository
- [x] Create .gitignore
- [x] Create README.md with setup instructions
- [x] Move plan to docs/roadmap.md
- [x] Create phase-based documentation structure
- [x] Create progress tracking system (PROGRESS.md)
- [x] Create Phase 1 implementation plan with user setup instructions
- [x] Organize best practices files in docs/best-practices/
- [x] Create CLAUDE.md for future Claude instances
- [x] Add competition context to memory file
- [x] Document setup requirements and API key management
- [x] Initial commit

**Decisions Made**:
- Project name: "Momentum - Personal Wellness Coach"
- Documentation structure: Phase-based approach with individual phase files
- Progress tracking: PROGRESS.md file updated after each step
- Best practices: Kept in this repo under docs/best-practices/
- Competition: Concierge Agents track, targeting 8+ key concepts
- Setup: Comprehensive user instructions for reproducibility

**Blockers**: None

**Completed**: 2025-11-16

**Notes**: Phase 0 complete. Repository initialized with comprehensive documentation, competition requirements tracked, and Phase 1 ready for approval.

---

## Phase 1: Chat-Planner (MVA) ✅

**Goal**: Build a working conversational agent that generates personalized workout plans

**Tasks**:
- [x] Task 1: Project Setup (requirements.txt, .env.example, agent structure)
- [x] Task 2: Create WellnessChiefAgent with instruction prompt
- [ ] Task 3: Session State Management ⚠️ **DEFERRED** (see Session State Decision)
- [x] Task 4: Plan Generation Logic with flexible timeline
- [ ] Task 5: Testing & Evaluation ⚠️ **DEFERRED** (see Evaluation Decision)

**Technical Decisions**:
- **ADK Structure**: Uses `agents/agent.py` with `root_agent` export (ADK requirement)
- **Prompts as Python Modules**: Moved from text files to Python constants in `agents/prompts/` package for cleaner imports
- **Model Selection**: Using `gemini-2.5-flash` (latest stable model as of 2025-11-17)
- **Flexible Timeline**: Removed hardcoded 4-week constraint; agent now asks for user's target timeline/goal date
- **Session State Decision**: **Task 3 deferred to future phase** (see below)

**Key Refinements**:
1. Fixed ADK web directory structure (needed `agents/agent.py`, not standalone config)
2. Created `.env` symlink in `agents/` directory for ADK auto-loading
3. Refactored prompts from text files to Python modules
4. Updated to latest stable Gemini model (2.5 Flash)
5. Enhanced prompt to support variable-length programs (not just 4 weeks)
6. Created `docs/prompt-engineering.md` to track prompt refinements
7. Added retry configuration for API resilience (429, 500, 503, 504 errors)

**Session State Management Decision (Task 3)**:
- **Status**: Deferred to Phase 3 or 4
- **Rationale**:
  - Gemini 2.5 has 1M token context window - sufficient for Phase 1 conversations
  - Session state will be added when it serves a **different purpose** from permanent memory
  - Session state tracks temporary conversation context within a single session
  - Permanent memory (Firestore, Phase 3+) stores historical data across sessions
  - These are complementary features, not alternatives
- **Future Implementation**: Will add session state in Phase 3 or 4 when implementing Firestore integration
- **Note**: This is explicitly separate from the Memory Bank and permanent storage features

**Evaluation Decision (Task 5)**:
- **Status**: Deferred to Phase 2 or later
- **Rationale**:
  - ADK's `response_match_score` uses semantic similarity (embeddings), not substring matching
  - Minimal keyword-based expected responses result in low scores even when agent behavior is correct
  - Best practice is to export actual conversations from `adk web` UI as evalsets
  - Hand-written evalsets require full, realistic expected responses for semantic similarity to work
- **Current Testing Approach**: Manual testing via `adk web` interface
- **Future Implementation**:
  - Use `adk web` to test conversations interactively
  - Export successful conversations as evalsets using web UI export feature
  - Create evaluation sets with realistic expected responses
  - Implement in Phase 2 alongside InstructorAgent testing
- **Decision Date**: 2025-11-17

**Blockers**: None

**Started**: 2025-11-16
**Completed**: 2025-11-17

**Notes**:
- Core agent functionality complete and demo-able via `adk web`
- Agent successfully asks clarifying questions before generating plans
- Plans are personalized based on goal, experience level, availability, and timeline
- Prompt engineering best practices documented
- Retry configuration added for API failures
- Manual testing via web UI is the current validation approach
- Automated evaluation deferred to Phase 2 (will use web UI conversation exports)

---

## Phase 2: Instructor (Adding a Spoke) ✅

**Goal**: Add InstructorAgent to explain exercises and provide instructional resources

**Tasks**:
- [x] Create InstructorAgent with Google Search tool
- [x] Integrate InstructorAgent into WellnessChiefAgent via AgentTool
- [x] Test hub-and-spoke pattern with exercise questions
- [ ] Implement observability (LoggingPlugin) ⚠️ **DEFERRED to Phase 5+**
- [ ] Create evaluation sets ⚠️ **DEFERRED to Phase 5+**

**Technical Decisions**:
- **Hub-and-Spoke Pattern**: WellnessChiefAgent uses InstructorAgent as AgentTool
- **LLM-Based Orchestration**: Chief agent decides when to delegate to InstructorAgent
- **Google Search Integration**: InstructorAgent uses built-in `google_search` tool
- **Output Key**: Added `output_key="exercise_instructions"` for explicit state tracking
- **Observability Deferral**: Decided to defer logging/observability to Phase 5 when we have TrackerAgent
- **Evaluation Deferral**: Will implement comprehensive evaluation after memory/persistence features

**Key Refinements**:
1. Fixed AgentTool integration issues with explicit prompt instructions
2. Resolved empty response issue by adding "present COMPLETE response" guidance
3. Created modular spoke agent structure in `agents/spokes/` directory
4. Instruction prompt emphasizes single comprehensive responses (no partial answers)

**Blockers**: None

**Started**: 2025-11-18
**Completed**: 2025-11-18

**Notes**:
- Hub-and-spoke architecture proven and working
- InstructorAgent successfully provides exercise guidance with YouTube videos
- Multi-agent orchestration via AgentTool demonstrated
- Ready for persistence layer (Phase 4)
- Observability and evaluation deferred to reduce scope and maintain velocity

---

## Development Workflow

### Phase Workflow
1. **Plan Phase**: Create detailed `docs/phases/phase-{N}.md` with tasks
2. **Approve Plan**: Review and approve implementation approach
3. **Implement**: Execute tasks following the phase plan
4. **Test**: Create evaluation set for the phase
5. **Demo**: Verify feature is working and demo-able
6. **Complete Phase**: Update PROGRESS.md and roadmap.md
7. **Review**: Document learnings and adjust future phases if needed

### File Update Protocol
- **After Each Task**: Update PROGRESS.md current phase section
- **After Phase Completion**: Update phase table and roadmap.md
- **Before Implementation**: Get approval on phase plan
- **After Completion**: Get approval that phase is complete

### Setup Documentation Requirements
- **User-Facing Instructions**: For any setup that Claude cannot do (Firebase, API keys, deployment), provide explicit step-by-step instructions in the relevant phase file
- **Reproducibility**: All setup must be documented so other users can clone and run the project
- **API Key Management**: Use `.env.example` templates, document required keys in README and phase files
- **External Services**: Document account creation, configuration, and integration steps

### Reference Documentation Usage
- **Efficiency**: Use Table of Contents in `docs/best-practices/best-practices.md` to find relevant sections
- **Don't Parse Entire Documents**: Navigate to specific sections using ToC instead of reading everything
- **Context Management**: Only read the sections needed for current task to preserve token budget

### Code Quality Guidelines
- **Minimal Comments**: Only explain WHY, not WHAT. Code should be self-explanatory through clear naming
- **Review After Every Change**: Remove unnecessary comments, reduce logging, clean up verbosity
- **No Redundant Documentation**: Avoid repeating what the code already says

---

## Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-11-16 | Submit to Concierge Agents track | Wellness coach is for personal use, fits track perfectly |
| 2025-11-16 | Target all 8+ key course concepts | Maximize technical implementation score (50 points) |
| 2025-11-16 | Plan for video submission | 10 bonus points for <3min demo video |
| 2025-11-16 | Use phase-based documentation approach | Allows incremental development with clear milestones |
| 2025-11-16 | Create PROGRESS.md as memory file | Tracks progress, decisions, and competition requirements |
| 2025-11-16 | Rename plan.md to roadmap.md | Better reflects the high-level nature of the document |
| 2025-11-17 | Use `agents/agent.py` with `root_agent` export | ADK web requires this structure, not standalone config file |
| 2025-11-17 | Prompts as Python modules in `agents/prompts/` | Cleaner than file I/O, easier imports, better IDE support |
| 2025-11-17 | Use `gemini-2.5-flash` model | Latest stable Gemini model as of implementation date |
| 2025-11-17 | Remove hardcoded 4-week timeline | Users need flexibility for different program lengths and goal dates |
| 2025-11-17 | Defer Task 3 (Session State) to later phase | 1M token context sufficient for Phase 1; will add when it serves different purpose from permanent memory |
| 2025-11-17 | Defer Task 5 (Evaluation) to Phase 2+ | ADK eval requires web UI conversation exports for realistic expected responses; hand-written evalsets fail semantic similarity scoring |
| 2025-11-18 | Defer Phase 2 observability to Phase 5+ | Focus on core features first; bundle observability with TrackerAgent logging |
| 2025-11-18 | Defer Phase 2 evaluation to Phase 5+ | Implement comprehensive evaluation after memory/persistence foundation |
| 2025-11-18 | **SKIP Phase 3 entirely** | Day 3 course materials show DatabaseSessionService MUST come before custom persistence; ADK Memory system replaces custom Firestore tools for conversation data |
| 2025-11-18 | Combine Sessions + Memory + LROs into Phase 4 | Follow course best practices: DatabaseSessionService → InMemoryMemoryService → LROs in single phase |
| 2025-11-18 | Use ADK Memory for conversation context | Automated consolidation, semantic search, cross-session recall; reserve Firestore for structured fitness data only |
| 2025-11-18 | Migrate to DatabaseSessionService in Phase 4 | Required prerequisite for LROs; InMemorySessionService insufficient for production |

---

## Phase 3: Plan Persister ⚠️ **SKIPPED**

**Status**: Skipped based on Day 3 course learnings

**Original Goal**: Save workout plans to Firestore with custom tools

**Why Skipped**:
1. **DatabaseSessionService Required First**: Course materials (Day 3a) show DatabaseSessionService migration MUST happen before any persistent storage implementation
2. **ADK Memory Replaces Custom Tools**: Day 3b demonstrates that `MemoryService` with automatic consolidation provides better architecture than custom Firestore tools for conversation/preference data
3. **Avoid Duplication**: Custom Firestore tools would duplicate what ADK's memory system already provides
4. **Better Separation of Concerns**:
   - **ADK Memory**: User preferences, conversation context, exercise history (automated, semantic search)
   - **Firestore**: Structured workout plans, nutrition logs, analytics (when needed in Phase 5-7)

**New Approach**:
- Phase 4 implements DatabaseSessionService + InMemoryMemoryService + automated memory callbacks
- Firestore added later (Phase 5-7) for structured fitness data that requires specific schema/queries
- Follows course best practices: Sessions → Memory → Structured Storage

**Decision Date**: 2025-11-18


---

## Phase 4: Sessions, Memory & LROs (Partial) 🔄

**Goal**: Establish production-ready persistence with DatabaseSessionService, Memory consolidation, and Exercise Plan Storage

**Status**: Goals 1-3 Complete (LROs deferred)

**Tasks**:
- [x] **Goal 1**: Persistent Sessions (DatabaseSessionService)
  - [x] Configure DatabaseSessionService with SQLite backend
  - [x] Verify session persistence across restarts
- [x] **Goal 2**: User Memory (InMemoryMemoryService)
  - [x] Configure InMemoryMemoryService
  - [x] Add preload_memory tool and auto_save_to_memory callback
  - [x] Verify memory recall across different sessions
- [x] **Goal 3**: Exercise Plan Storage
  - [x] Create 4 plan tools (save_plan, load_plan, get_current_week_plan, list_user_plans)
  - [x] Implement Firestore-compatible JSON schema
  - [x] Verify plan persistence and retrieval
- [ ] **Goal 4**: Long-Running Operations (LROs) - **DEFERRED**

**Technical Decisions**:
- **Sessions**: DatabaseSessionService with SQLite (`data/wellness_sessions.db`)
- **Memory**: InMemoryMemoryService with automatic consolidation via callbacks
- **Plan Storage**: File-based JSON with Firestore-compatible schema for Phase 5-7 migration
- **Schema Design**: Matches roadmap's Firestore `plan` collection (lines 467-476)
- **Migration Path**: File I/O → Firestore CRUD (same schema, minimal code changes)

**Key Achievements**:
1. **Session Persistence**: Conversations survive application restarts
2. **Cross-Session Memory**: Agent recalls user facts across different conversations
3. **Plan Storage**: Structured workout plans persist with query capabilities
4. **Future-Proof Design**: JSON schema enables seamless Firestore migration

**Files Modified**:
- `agents/agent.py`: Added DatabaseSessionService and InMemoryMemoryService
- `agents/hub.py`: Added preload_memory, auto_save_to_memory, and plan tools
- `agents/prompts/wellness_chief.py`: Added Plan Storage instructions
- `agents/tools/plan_tools.py`: Created 4 plan storage tools
- `.gitignore`: Added data/ directory exclusion

**Migration Documentation**:
- **Current**: File-based JSON in `data/plans/{user_id}/`
- **Phase 5-7**: Firestore CRUD with same schema
- **Migration Steps**:
  1. Create `core/database.py` with Firestore client
  2. Replace file I/O with Firestore CRUD in `plan_tools.py`
  3. Keep same function signatures (no tool interface changes)
  4. Keep same JSON schema (no data transformation)
  5. One-time script to migrate existing JSON files

**Blockers**: None

**Started**: 2025-11-23
**Completed**: Goals 1-3 on 2025-11-23

**Notes**:
- LROs (Goal 4) deferred to allow focused implementation of persistence layer
- Memory system uses InMemoryMemoryService (will migrate to Vertex AI Memory Bank in Phase 11)
- Plan storage designed for zero-friction Firestore migration
- All 3 goals verified with automated test scripts

---

## Next Steps

1. ✅ Review Day 3 course notebooks for sessions/memory best practices
2. ✅ Update PROGRESS.md with Phase 2 completion
3. ✅ Document architectural pivot (skip Phase 3)
4. ✅ Create Phase 4 implementation plan (Sessions + Memory + LROs combined)
5. ✅ Implement Goals 1-3 (Sessions, Memory, Plan Storage)
6. 🔄 Commit Phase 4 Goals 1-3
7. 🔄 Decide on LROs implementation (Goal 4) or proceed to Phase 5

