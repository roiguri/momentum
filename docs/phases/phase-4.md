# Phase 4: Sessions, Memory & LROs (Combined)

**Status**: ⚪ Not Started
**Priority**: P0 (Critical Foundation)
**Estimated Effort**: 6-8 hours
**Started**: TBD
**Completed**: TBD

---

## Overview

**Goal**: Establish production-ready persistence layer with DatabaseSessionService, Memory consolidation, and Long-Running Operations for calendar scheduling.

**Demo**:
1. User creates workout plan → automatically saved to memory across sessions
2. User asks "What was my goal?" in new session → agent recalls from memory
3. User approves calendar scheduling → LRO workflow with user confirmation

**Key Concepts**:
- Session Management (DatabaseSessionService migration)
- Long-term Memory (InMemoryMemoryService with callbacks)
- Long-Running Operations (LRO with user approval)
- MCP Tools (Google Calendar integration)
- Context Engineering (session state + memory)

**Course Alignment**: Day 3 (Sessions & Memory), Day 4 (LROs)

---

## Why This Phase Combines Three Features

Based on Day 3 course materials, these features form a **logical dependency chain**:

1. **DatabaseSessionService** → Required for LROs (InMemorySessionService insufficient)
2. **Memory System** → Natural pairing with persistent sessions
3. **LROs** → Demonstrates the full system working together

**Benefits**:
- Single migration eliminates future refactoring
- Follows course best practices (sessions → memory → LROs)
- Creates solid foundation for all future phases

---

## Prerequisites

### From Previous Phases
- [x] WellnessChiefAgent working (Phase 1)
- [x] InstructorAgent as spoke (Phase 2)
- [x] Hub-and-spoke pattern proven

### New Requirements
- [ ] Review Day 3a notebook (Sessions) in `course-notebooks/day-3/`
- [ ] Review Day 3b notebook (Memory) in `course-notebooks/day-3/`
- [ ] Review Day 4 materials on LROs (if available)
- [ ] Understand DatabaseSessionService migration pattern
- [ ] Familiarize with callback system for auto-memory

### User Setup Tasks (Cannot be done by Claude)
- [ ] Install Google Calendar MCP server (instructions in Task 4)
- [ ] Authorize Google Calendar API access
- [ ] Test MCP server connection

---

## Implementation Tasks

### Task 1: Migrate to DatabaseSessionService ✅

**Goal**: Replace InMemorySessionService with SQLite-backed persistent sessions

**Acceptance Criteria**:
- ✅ Sessions survive application restarts
- ✅ Conversation history persists across runs
- ✅ No breaking changes to existing agent functionality
- ✅ Test with existing WellnessChiefAgent + InstructorAgent

**Implementation Steps**:

1. **Update session configuration** in `agents/agent.py`:
   ```python
   from google.adk.sessions import DatabaseSessionService

   session_service = DatabaseSessionService(
       db_url="sqlite:///data/wellness_sessions.db"
   )
   ```

2. **Create data directory**:
   ```bash
   mkdir -p data
   echo "data/*.db" >> .gitignore  # Don't commit database files
   ```

3. **Update Runner initialization**:
   ```python
   runner = Runner(
       agent=root_agent,
       app_name="momentum",
       session_service=session_service  # Now using DatabaseSessionService
   )
   ```

4. **Test migration**:
   - Start `adk web`
   - Have a conversation with exercise questions
   - Stop and restart `adk web`
   - Resume same session - conversation should persist

**Reference**:
- `course-notebooks/day-3/day-3a-agent-sessions.ipynb` Section 3
- `docs/best-practices/best-practices.md` - Session Management section

**Estimated Time**: 1 hour

---

### Task 2: Implement Memory System with Auto-Save ✅

**Goal**: Add InMemoryMemoryService with automatic memory consolidation via callbacks

**Acceptance Criteria**:
- ✅ Memory service initialized and connected to Runner
- ✅ Conversations automatically saved to memory after each turn
- ✅ Agent can retrieve memories from previous sessions
- ✅ `preload_memory` tool integrated for automatic recall

**Implementation Steps**:

1. **Add memory service initialization** in `agents/agent.py`:
   ```python
   from google.adk.memory import InMemoryMemoryService
   from google.adk.tools import preload_memory

   memory_service = InMemoryMemoryService()
   ```

2. **Create auto-save callback**:
   ```python
   async def auto_save_to_memory(callback_context):
       """Automatically save session to memory after each agent turn."""
       await callback_context._invocation_context.memory_service.add_session_to_memory(
           callback_context._invocation_context.session
       )
   ```

3. **Update WellnessChiefAgent** in `agents/hub.py`:
   ```python
   wellness_chief = LlmAgent(
       name="WellnessChiefAgent",
       instruction=WELLNESS_CHIEF_PROMPT,
       tools=[
           AgentTool(agent=instructor_agent),
           preload_memory  # Add memory retrieval tool
       ],
       after_agent_callback=auto_save_to_memory  # Auto-save to memory
   )
   ```

4. **Update Runner** to provide both services:
   ```python
   runner = Runner(
       agent=root_agent,
       app_name="momentum",
       session_service=session_service,
       memory_service=memory_service  # Add memory service
   )
   ```

5. **Update WellnessChiefAgent prompt** to leverage memory:
   ```python
   WELLNESS_CHIEF_PROMPT = """
   You are a personal wellness coach...

   Use the preload_memory tool to recall user preferences, goals, and past conversations.
   This helps you provide personalized guidance without asking repetitive questions.

   [rest of prompt...]
   """
   ```

**Testing**:
- Session 1: Tell agent "My goal is to run a 5k in under 25 minutes"
- Session 2 (new session_id): Ask "What was my goal?" → should recall from memory
- Session 3: Ask for plan → should use remembered goal without re-asking

**Reference**:
- `course-notebooks/day-3/day-3b-agent-memory.ipynb` Sections 3-6
- `docs/best-practices/best-practices.md` - Memory Management section

**Estimated Time**: 2 hours

---

### Task 3: Add Session State for Temporary Data ✅

**Goal**: Implement session state for conversation-scoped temporary data (complementary to long-term memory)

**Acceptance Criteria**:
- ✅ Session state used for temporary conversation flow tracking
- ✅ Clear distinction between session.state (temporary) and memory (permanent)
- ✅ State keys use prefixes (user:, temp:, app:)

**Implementation Steps**:

1. **Create state management tools** in `agents/tools/state_tools.py`:
   ```python
   from google.adk.tools.tool_context import ToolContext
   from typing import Dict, Any

   def save_temp_preference(
       tool_context: ToolContext,
       key: str,
       value: str
   ) -> Dict[str, Any]:
       """Save temporary preference to session state."""
       tool_context.state[f"temp:{key}"] = value
       return {"status": "success", "key": key}

   def get_temp_preference(
       tool_context: ToolContext,
       key: str
   ) -> Dict[str, Any]:
       """Retrieve temporary preference from session state."""
       value = tool_context.state.get(f"temp:{key}", None)
       return {"status": "success", "value": value}
   ```

2. **Update WellnessChiefAgent** with state tools:
   ```python
   from .tools.state_tools import save_temp_preference, get_temp_preference

   wellness_chief = LlmAgent(
       tools=[
           AgentTool(agent=instructor_agent),
           preload_memory,
           save_temp_preference,  # Session state management
           get_temp_preference
       ],
       after_agent_callback=auto_save_to_memory
   )
   ```

3. **Update prompt** to explain state vs memory:
   ```python
   WELLNESS_CHIEF_PROMPT = """
   ...

   State Management:
   - Use session state (save_temp_preference) for temporary conversation data
   - Use memory (preload_memory) for long-term user preferences

   Example: Current workout intensity → session state
   Example: User's fitness goal → memory (permanent)
   """
   ```

**Testing**:
- Save temporary workout intensity during plan creation
- Verify state accessible within same session
- Verify state cleared in new session (expected behavior)

**Reference**:
- `course-notebooks/day-3/day-3a-agent-sessions.ipynb` Section 5
- `docs/best-practices/best-practices.md` - State Management section

**Estimated Time**: 1.5 hours

---

### Task 4: Implement LRO with Google Calendar ✅

**Goal**: Add calendar scheduling with user approval workflow (Long-Running Operation)

**Acceptance Criteria**:
- ✅ Agent asks user for approval before calendar modifications
- ✅ User can approve/reject calendar scheduling
- ✅ Approved plans added to Google Calendar
- ✅ Rejected requests handled gracefully
- ✅ LRO workflow properly suspends/resumes agent

**User Setup Instructions** (Cannot be automated):

1. **Install Google Calendar MCP Server**:
   ```bash
   # Follow MCP documentation for Google Calendar server setup
   # This typically involves:
   # 1. Installing the MCP server
   # 2. Configuring OAuth credentials
   # 3. Adding server to MCP config
   ```

2. **Authorize Calendar Access**:
   - Run MCP server authorization flow
   - Grant calendar read/write permissions
   - Test connection with simple calendar query

3. **Verify MCP Server**:
   ```bash
   # Test that MCP server is accessible
   # Document the server name/endpoint for agent configuration
   ```

**Implementation Steps**:

1. **Create SchedulerAgent** in `agents/spokes/scheduler.py`:
   ```python
   from google.adk.agents import LlmAgent
   from google.adk.models import Gemini
   from google.adk.tools.tool_context import ToolContext

   def create_scheduler_agent(calendar_tool):
       """Create SchedulerAgent with Google Calendar MCP tool."""
       return LlmAgent(
           name="SchedulerAgent",
           description="Schedules workout sessions in Google Calendar",
           instruction="""
           You help schedule workout plans in the user's Google Calendar.

           When given a workout plan:
           1. Create calendar events for each workout session
           2. Include exercise details in event description
           3. Set appropriate duration (usually 45-60 minutes)
           4. Confirm successful scheduling
           """,
           tools=[calendar_tool],
           output_key="calendar_status"
       )
   ```

2. **Add LRO confirmation tool** in `agents/tools/lro_tools.py`:
   ```python
   async def request_calendar_approval(
       tool_context: ToolContext,
       plan_summary: str
   ) -> Dict[str, Any]:
       """Request user approval for calendar scheduling (LRO)."""
       approval = await tool_context.request_confirmation(
           prompt=f"""
           I've created your workout plan:

           {plan_summary}

           Would you like me to add these workouts to your Google Calendar?
           """,
           title="Calendar Scheduling Approval"
       )

       return {
           "approved": approval,
           "message": "User approved" if approval else "User declined"
       }
   ```

3. **Update WellnessChiefAgent** with scheduler + LRO:
   ```python
   from .spokes.scheduler import create_scheduler_agent
   from .tools.lro_tools import request_calendar_approval

   # Initialize calendar MCP tool (configuration TBD based on MCP setup)
   # calendar_tool = ...  # MCP tool instance

   scheduler_agent = create_scheduler_agent(calendar_tool)

   wellness_chief = LlmAgent(
       tools=[
           AgentTool(agent=instructor_agent),
           AgentTool(agent=scheduler_agent),
           preload_memory,
           save_temp_preference,
           get_temp_preference,
           request_calendar_approval  # LRO tool
       ],
       after_agent_callback=auto_save_to_memory
   )
   ```

4. **Update prompt** for LRO workflow:
   ```python
   WELLNESS_CHIEF_PROMPT = """
   ...

   Calendar Scheduling Workflow:
   1. After creating a workout plan, summarize it for the user
   2. Use request_calendar_approval to ask for permission
   3. If approved, delegate to SchedulerAgent to add events
   4. If declined, save plan to memory but skip calendar

   IMPORTANT: Always get explicit user approval before modifying their calendar.
   """
   ```

**Testing LRO Workflow**:
1. Create workout plan via conversation
2. Agent requests approval → LRO suspends
3. User approves → LRO resumes
4. SchedulerAgent adds events to calendar
5. Verify events appear in Google Calendar

**Reference**:
- Course Day 4 materials on LROs
- `docs/best-practices/best-practices.md` - Long-Running Operations section
- MCP Google Calendar documentation

**Estimated Time**: 3 hours (including MCP setup)

---

### Task 5: Testing & Validation ✅

**Goal**: Comprehensive testing of all Phase 4 features working together

**Test Scenarios**:

1. **Session Persistence Test**:
   - Start conversation, create plan
   - Stop `adk web`
   - Restart `adk web`
   - Resume conversation → should maintain context

2. **Memory Across Sessions Test**:
   - Session 1: "My goal is marathon training, I run 3x/week"
   - Session 2 (new ID): "Create a plan for me" → should recall goal without asking

3. **Session State vs Memory Test**:
   - Verify temporary data (current intensity) in session.state
   - Verify permanent data (fitness goal) in memory
   - New session should NOT have temp data, SHOULD have permanent data

4. **LRO Approval Workflow Test**:
   - Create plan
   - Decline calendar approval → plan saved to memory, no calendar events
   - Create another plan
   - Approve calendar → events appear in Google Calendar

5. **Multi-Agent Integration Test**:
   - Ask exercise question → InstructorAgent responds
   - Create plan → saved to memory
   - Schedule plan → SchedulerAgent + LRO workflow

**Acceptance Criteria**:
- ✅ All test scenarios pass
- ✅ No data loss on restart
- ✅ Memory retrieval works cross-session
- ✅ LRO approval/rejection both handled correctly
- ✅ All agents work together seamlessly

**Estimated Time**: 1.5 hours

---

## Architecture Diagrams

### Session + Memory Architecture

```
┌─────────────────────────────────────────────────────┐
│                  WellnessChiefAgent                  │
│  ┌────────────────────────────────────────────┐    │
│  │ Tools:                                      │    │
│  │ - InstructorAgent (AgentTool)              │    │
│  │ - SchedulerAgent (AgentTool)               │    │
│  │ - preload_memory (auto-retrieval)          │    │
│  │ - save_temp_preference (session state)     │    │
│  │ - request_calendar_approval (LRO)          │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Callbacks:                                          │
│  - after_agent_callback → auto_save_to_memory       │
└─────────────────────────────────────────────────────┘
                        ↓
              ┌─────────────────┐
              │     Runner      │
              │                 │
              │ ┌─────────────┐ │
              │ │  Session    │ │
              │ │  Service    │ │ ← DatabaseSessionService (SQLite)
              │ └─────────────┘ │
              │                 │
              │ ┌─────────────┐ │
              │ │   Memory    │ │
              │ │  Service    │ │ ← InMemoryMemoryService
              │ └─────────────┘ │
              └─────────────────┘
```

### LRO Workflow

```
User: "Create a 5k training plan"
  ↓
WellnessChief generates plan
  ↓
WellnessChief calls request_calendar_approval()
  ↓
LRO SUSPENDS (agent pauses)
  ↓
User sees approval prompt
  ↓
[User Decision]
  ├─ APPROVE → LRO RESUMES
  │             ↓
  │    WellnessChief calls SchedulerAgent
  │             ↓
  │    Events added to Google Calendar
  │
  └─ DECLINE → LRO RESUMES
                ↓
       Plan saved to memory only
```

---

## Phase Completion Checklist

### Code Implementation
- [ ] DatabaseSessionService migration complete
- [ ] InMemoryMemoryService initialized
- [ ] Auto-save callback implemented
- [ ] preload_memory tool integrated
- [ ] Session state tools created
- [ ] SchedulerAgent created
- [ ] LRO approval tool implemented
- [ ] WellnessChiefAgent updated with all tools

### Testing
- [ ] Session persistence verified
- [ ] Memory recall across sessions verified
- [ ] Session state vs memory distinction tested
- [ ] LRO approval workflow tested
- [ ] LRO rejection workflow tested
- [ ] Multi-agent integration tested

### Documentation
- [ ] Update PROGRESS.md with completion
- [ ] Document any issues/learnings
- [ ] Update roadmap.md if architecture changed
- [ ] Create .env.example for calendar credentials (if applicable)

### User Setup
- [ ] Google Calendar MCP server setup instructions documented
- [ ] OAuth authorization process documented
- [ ] Testing instructions for calendar integration

---

## Success Metrics

**Must Have**:
1. Sessions persist across restarts (DatabaseSessionService working)
2. Memory recalls user preferences from previous sessions
3. LRO approval workflow works end-to-end
4. Calendar events successfully created when approved

**Should Have**:
1. Session state used appropriately for temporary data
2. Clear separation between session state and memory
3. All spoke agents (Instructor, Scheduler) work in harmony

**Nice to Have**:
1. Memory consolidation patterns identified (prepares for Vertex AI migration)
2. Performance baseline established (session/memory retrieval speed)

---

## Known Limitations & Future Work

### InMemoryMemoryService Limitations
- **Keyword matching only** (no semantic search)
- **No persistence** (resets on restart)
- **No consolidation** (stores raw conversation data)

**Migration Path**: Phase 11 will migrate to Vertex AI Memory Bank for:
- Semantic search (meaning-based retrieval)
- LLM-powered consolidation (extract key facts)
- Cloud persistence (survives restarts)

### Firestore Integration
- **Deferred to Phase 5-7** for structured fitness data
- Use cases: Workout logs, nutrition tracking, analytics
- Complements Memory (structured data vs conversation context)

---

## Reference Materials

**Course Notebooks**:
- `course-notebooks/day-3/day-3a-agent-sessions.ipynb` - Sessions
- `course-notebooks/day-3/day-3b-agent-memory.ipynb` - Memory
- `course-notebooks/day-4/` - LROs (if available)

**Best Practices**:
- `docs/best-practices/best-practices.md` - Session Management section
- `docs/best-practices/best-practices.md` - Memory Management section
- `docs/best-practices/best-practices.md` - Long-Running Operations section

**ADK Documentation**:
- [Sessions](https://google.github.io/adk-docs/sessions/)
- [Memory](https://google.github.io/adk-docs/sessions/memory/)
- [Callbacks](https://google.github.io/adk-docs/agents/callbacks/)

---

## Notes

This phase represents a **critical architectural foundation**. All future phases depend on:
- Persistent sessions (for conversation continuity)
- Memory system (for personalization)
- LRO workflow (for safe external integrations)

Take time to test thoroughly before moving to Phase 5.
