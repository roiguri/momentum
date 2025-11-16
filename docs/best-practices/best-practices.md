# AI Agents Best Practices

## Table of Contents
- [Agent Architecture Design](#agent-architecture-design)
- [Workflow Pattern Selection](#workflow-pattern-selection)
  - [Sequential Agents: For Ordered Pipelines](#sequential-agents-for-ordered-pipelines)
  - [Parallel Agents: For Concurrent Execution](#parallel-agents-for-concurrent-execution)
  - [Loop Agents: For Iterative Refinement](#loop-agents-for-iterative-refinement)
  - [LLM-Based Orchestration: For Dynamic Workflows](#llm-based-orchestration-for-dynamic-workflows)
- [State Management](#state-management)
- [Instructions Best Practices](#instructions-best-practices)
- [Error Handling](#error-handling)
- [Loop Agent Implementation](#loop-agent-implementation)
- [Tool Integration](#tool-integration)
  - [Custom Function Tools](#custom-function-tools)
  - [Agent Tools](#agent-tools)
  - [MCP Tools](#mcp-tools)
  - [Code Execution Tools](#code-execution-tools)
  - [Long-Running Operations](#long-running-operations)
- [Session Management](#session-management)
- [Context Engineering](#context-engineering)
- [Memory Management](#memory-management)
- [Callbacks](#callbacks)
- [Observability and Evaluation](#observability-and-evaluation)
- [Agent2Agent Communication](#agent2agent-communication)
- [Production Deployment](#production-deployment)
- [Runner and Session Management](#runner-and-session-management)
- [Development and Debugging](#development-and-debugging)
- [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)

## Agent Architecture Design

### DO: Use Multi-Agent Systems for Complex Tasks
```python
# Good: Specialized agents with clear responsibilities
research_agent = Agent(
    name="ResearchAgent",
    instruction="Your only job is to use google_search to find 2-3 relevant pieces of information",
    tools=[google_search],
    output_key="research_findings"
)

summarizer_agent = Agent(
    name="SummarizerAgent",
    instruction="Read the provided research findings: {research_findings}. Create a concise summary.",
    output_key="final_summary"
)
```

### DON'T: Create Monolithic Agents
```python
# Bad: One agent trying to do everything
monolithic_agent = Agent(
    name="DoEverything",
    instruction="Research the topic, write a summary, edit it, fact-check it, and format it",
    tools=[google_search, other_tools...]  # Too many responsibilities
)
```

## Workflow Pattern Selection

### Sequential Agents: For Ordered Pipelines
Use when each step must complete before the next begins.

```python
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent]
)
```

**When to use:**
- Order matters
- Each step builds on previous results
- Linear, deterministic flow needed

### Parallel Agents: For Concurrent Execution
Use when tasks are independent and can run simultaneously.

```python
parallel_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher]
)

# Typically followed by an aggregator
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_team, aggregator_agent]
)
```

**When to use:**
- Tasks are independent
- Speed is important
- Multiple data sources need to be queried simultaneously

### Loop Agents: For Iterative Refinement
Use when output needs multiple rounds of review and improvement.

```python
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2
)
```

**When to use:**
- Quality improvement through iteration
- Feedback and revision cycles needed
- Output requires refinement

### LLM-Based Orchestration: For Dynamic Workflows
Use when the workflow needs dynamic decision-making.

```python
root_agent = Agent(
    name="Coordinator",
    instruction="Call ResearchAgent first, then call SummarizerAgent with the results",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)]
)
```

**When to use:**
- Workflow depends on runtime conditions
- LLM needs to decide which tools to call

**Warning:** This pattern can be unpredictable. For guaranteed order, use SequentialAgent instead.

## State Management

### DO: Use output_key and Placeholders
```python
# First agent stores its output
agent1 = Agent(
    name="Agent1",
    instruction="Generate a report",
    output_key="report"
)

# Second agent uses the output via placeholder
agent2 = Agent(
    name="Agent2",
    instruction="Summarize this report: {report}",
    output_key="summary"
)
```

### DON'T: Hardcode Data or Skip State Passing
```python
# Bad: No state sharing mechanism
agent2 = Agent(
    instruction="Summarize the report"  # Which report? No context!
)
```

## Instructions Best Practices

### DO: Be Specific and Clear
```python
agent = Agent(
    instruction="""You are a specialized research agent. Your only job is to:
    1. Use the google_search tool
    2. Find 2-3 pieces of relevant information
    3. Present findings with citations"""
)
```

### DO: Specify Output Format
```python
agent = Agent(
    instruction="""Create a concise summary as a bulleted list with 3-5 key points."""
)
```

### DO: Provide Tool Usage Guidance
```python
agent = Agent(
    instruction="""You are a helpful assistant. Use Google Search for current info or if unsure.""",
    tools=[google_search]
)
```

### DON'T: Write Vague Instructions
```python
# Bad: Unclear expectations
agent = Agent(
    instruction="Help with research"
)
```

## Error Handling

### DO: Configure Retry Options
```python
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,              # Maximum retry attempts
    exp_base=7,              # Delay multiplier for exponential backoff
    initial_delay=1,         # Initial delay before first retry (seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    )
)
```

**Purpose:** Handles transient errors like rate limits and temporary service unavailability automatically.

## Loop Agent Implementation

### DO: Implement Proper Exit Conditions
```python
# 1. Define exit function
def exit_loop():
    """Call when refinement is complete"""
    return {"status": "approved", "message": "Refinement complete"}

# 2. Create critic agent with clear approval signal
critic_agent = Agent(
    instruction="""Review the story: {current_story}
    - If well-written, respond with EXACTLY: "APPROVED"
    - Otherwise, provide 2-3 specific suggestions"""
)

# 3. Create refiner agent with exit tool
refiner_agent = Agent(
    instruction="""
    Story: {current_story}
    Critique: {critique}

    IF critique is EXACTLY "APPROVED", call exit_loop function
    OTHERWISE, rewrite the story incorporating the feedback""",
    tools=[FunctionTool(exit_loop)],
    output_key="current_story"  # Overwrites with refined version
)

# 4. Set max_iterations to prevent infinite loops
loop_agent = LoopAgent(
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2
)
```

### DON'T: Create Loops Without Exit Conditions
```python
# Bad: No way to exit, will run until max_iterations
loop_agent = LoopAgent(
    sub_agents=[writer_agent, editor_agent],
    max_iterations=10  # Will always run 10 times
)
```

## Tool Integration

### Custom Function Tools

### DO: Follow Function Tool Best Practices
```python
def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: The ISO 4217 currency code you're converting from (e.g., "USD")
        target_currency: The ISO 4217 currency code you're converting to (e.g., "EUR")

    Returns:
        Dictionary with status and rate information.
        Success: {"status": "success", "rate": 0.93}
        Error: {"status": "error", "error_message": "Unsupported currency pair"}
    """
    rate_database = {"usd": {"eur": 0.93, "jpy": 157.50}}

    base = base_currency.lower()
    target = target_currency.lower()

    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}"
        }
```

**Why this is good:**
- ✅ Clear docstring (LLMs use this to understand when/how to use the tool)
- ✅ Type hints (`str`, `dict`) for proper schema generation
- ✅ Dictionary returns with `status` field
- ✅ Structured error handling

### DON'T: Create Poorly Documented Tools
```python
# Bad: No docstring, no type hints, unclear return format
def exchange(a, b):
    return 0.93  # Which currency? What if error?
```

### DO: Use Structured Return Values
```python
# Good: Consistent structure with status indicator
return {"status": "success", "data": result}
return {"status": "error", "error_message": "Description"}
```

### DON'T: Return Inconsistent Formats
```python
# Bad: Inconsistent returns
def my_tool(param):
    if success:
        return result  # Sometimes a value
    else:
        return None  # Sometimes None
        # or raise Exception  # Sometimes an exception
```

### Agent Tools

### DO: Use Agents as Tools for Delegation
```python
# Create specialist agent
calculation_agent = LlmAgent(
    name="CalculationAgent",
    instruction="Generate Python code to calculate the result. Print the final result.",
    code_executor=BuiltInCodeExecutor()
)

# Use specialist as a tool in main agent
main_agent = LlmAgent(
    name="MainAgent",
    instruction="Use calculation_agent to perform accurate calculations",
    tools=[AgentTool(agent=calculation_agent)]
)
```

**When to use Agent Tools:**
- You need specialized processing (calculations, analysis)
- The sub-agent's result should return to the calling agent
- Building modular, reusable agent components

### DO: Understand Agent Tools vs Sub-Agents
```python
# Agent Tools: Response returns to caller
main_agent = LlmAgent(
    tools=[AgentTool(specialist_agent)]  # Specialist does work, returns result
)

# Sub-Agents: Complete control transfer (different pattern)
# Use for handoff scenarios, not delegation
```

### MCP Tools

### DO: Connect to MCP Servers for External Services
```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Connect to MCP server
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"]  # Only use specific tools
        ),
        timeout=30
    )
)

agent = LlmAgent(
    name="ImageAgent",
    instruction="Use the MCP Tool to generate images",
    tools=[mcp_toolset]
)
```

**When to use MCP Tools:**
- External service integration (GitHub, databases, file systems)
- Community-built tools are available
- Standardized interface across different services

### DON'T: Build Custom Integrations When MCP Exists
```python
# Bad: Writing custom API client
def my_github_integration():
    # 100+ lines of custom code...
    pass

# Good: Use existing MCP server
github_mcp = McpToolset(connection_params=...)
```

### Code Execution Tools

### DO: Use Code Execution for Reliable Calculations
```python
# Create calculation agent with code executor
calculation_agent = LlmAgent(
    name="CalculationAgent",
    instruction="""Generate Python code to calculate the result.
    Rules:
    1. Output ONLY a Python code block
    2. Do NOT perform calculations yourself
    3. The code MUST print the final result""",
    code_executor=BuiltInCodeExecutor()
)

# Main agent delegates math to code execution
main_agent = LlmAgent(
    instruction="Use calculation_agent for all arithmetic calculations",
    tools=[AgentTool(agent=calculation_agent)]
)
```

**Why:** LLMs are unreliable at arithmetic. Code execution provides deterministic, accurate results.

### DON'T: Rely on LLM for Complex Math
```python
# Bad: Asking LLM to do calculations
agent = LlmAgent(
    instruction="Calculate the final amount after applying 2.5% fee to $1,234.56"
    # LLM may make calculation errors
)
```

### Long-Running Operations

### DO: Implement Human-in-the-Loop Approvals
```python
def place_order(num_items: int, tool_context: ToolContext) -> dict:
    """Places an order with approval for large quantities."""

    # Small orders: auto-approve
    if num_items <= 5:
        return {"status": "approved", "order_id": "AUTO-123"}

    # First call: Request approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Approve order for {num_items} items?",
            payload={"num_items": num_items}
        )
        return {"status": "pending", "message": "Awaiting approval"}

    # Second call: Handle approval response
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved", "order_id": "HUMAN-456"}
    else:
        return {"status": "rejected"}

# Wrap agent in resumable app
app = App(
    name="OrderSystem",
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
```

**When to use Long-Running Operations:**
- 💰 Financial transactions requiring approval
- 🗑️ Bulk operations (delete many records)
- ⚠️ Irreversible operations
- 💸 High-cost actions

### DO: Handle Approval Workflow Correctly
```python
async def run_with_approval(query: str, auto_approve: bool = True):
    # Step 1: Send initial request
    events = []
    async for event in runner.run_async(
        user_id="user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # Step 2: Check for approval request
    approval_info = check_for_approval_event(events)

    # Step 3: If approval needed, resume with decision
    if approval_info:
        approval_response = create_approval_response(approval_info, auto_approve)
        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=approval_response,
            invocation_id=approval_info["invocation_id"]  # Critical: same ID to resume
        ):
            process_event(event)
```

### DON'T: Forget invocation_id When Resuming
```python
# Bad: Missing invocation_id starts NEW execution instead of resuming
async for event in runner.run_async(
    new_message=approval_response
    # Missing invocation_id!
):
    pass
```

### General Tool Best Practices

### DO: Provide Only Necessary Tools
```python
# Good: Agent has only what it needs
research_agent = Agent(
    tools=[google_search]
)

# Good: Agent has no tools if it doesn't need them
summarizer_agent = Agent(
    tools=[]  # Or omit the tools parameter
)
```

### DO: Reference Tools by Exact Names in Instructions
```python
agent = LlmAgent(
    instruction="""Use get_fee_for_payment_method() to find fees.
    Use get_exchange_rate() to get rates.
    Check the 'status' field in each response for errors.""",
    tools=[get_fee_for_payment_method, get_exchange_rate]
)
```

## Session Management

### DO: Choose the Right SessionService

```python
# Development: InMemorySessionService (temporary)
session_service = InMemorySessionService()

# Production: DatabaseSessionService (persistent)
session_service = DatabaseSessionService(db_url="sqlite:///agent_data.db")

# Enterprise: Use Vertex AI Agent Engine
```

**When to use each:**
- **InMemorySessionService**: Quick prototyping, testing (data lost on restart)
- **DatabaseSessionService**: Production apps that need persistence
- **Vertex AI Agent Engine**: Enterprise scale with managed infrastructure

### DO: Create Stateful Agents Properly

```python
# Step 1: Create agent
agent = Agent(
    name="chatbot",
    model=Gemini(model="gemini-2.5-flash-lite")
)

# Step 2: Create session service
session_service = InMemorySessionService()

# Step 3: Create runner with session service
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service
)

# Step 4: Create and use sessions
session = await session_service.create_session(
    app_name="my_app",
    user_id="user123",
    session_id="conversation_01"
)
```

### DO: Use Session State for Conversation Data

```python
def save_userinfo(tool_context: ToolContext, user_name: str) -> dict:
    """Save user information to session state."""
    tool_context.state["user:name"] = user_name
    return {"status": "success"}

def retrieve_userinfo(tool_context: ToolContext) -> dict:
    """Retrieve user information from session state."""
    user_name = tool_context.state.get("user:name", "Not found")
    return {"status": "success", "user_name": user_name}

agent = LlmAgent(
    tools=[save_userinfo, retrieve_userinfo]
)
```

**Best practices for state keys:**
- Use prefixes: `user:`, `app:`, `temp:`
- Be descriptive: `user:preferred_language` not just `lang`
- Document what each key stores

### DON'T: Rely on Sessions Across Restarts with InMemorySessionService

```python
# Bad: Expecting data to persist after restart
session_service = InMemorySessionService()  # In-memory only!
# ... restart application ...
# Data is gone!

# Good: Use DatabaseSessionService for persistence
session_service = DatabaseSessionService(db_url="sqlite:///data.db")
# Data survives restarts
```

## Context Engineering

### DO: Implement Context Compaction for Long Conversations

```python
from google.adk.apps.app import App, EventsCompactionConfig

app = App(
    name="my_app",
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compact every 3 turns
        overlap_size=1  # Keep 1 previous turn for context
    )
)

runner = Runner(app=app, session_service=session_service)
```

**Why compaction matters:**
- Long conversations consume many tokens
- Compaction summarizes old turns to save costs
- Agent stays focused on recent context
- Improves performance and reduces latency

### DO: Configure Compaction Appropriately

```python
# For detailed conversations requiring more history
EventsCompactionConfig(
    compaction_interval=5,  # Less frequent compaction
    overlap_size=2  # More overlap for continuity
)

# For transactional conversations
EventsCompactionConfig(
    compaction_interval=2,  # Frequent compaction
    overlap_size=0  # Minimal overlap needed
)
```

### DO: Understand Compaction Process

1. Conversation reaches `compaction_interval` turns
2. ADK automatically triggers LLM-based summarization
3. Summary replaces older events in active context
4. Original events remain in database for audit
5. Future turns use compacted history

## Memory Management

### DO: Understand Session vs Memory

| Aspect | Session | Memory |
|--------|---------|--------|
| Scope | Single conversation | Cross-conversation |
| Duration | Temporary (conversation lifetime) | Long-term (persistent) |
| Purpose | Track current dialogue flow | Store knowledge facts |
| Storage | Events (messages, tool calls) | Consolidated information |

### DO: Implement Memory Service Properly

```python
from google.adk.memory import InMemoryMemoryService

# Step 1: Initialize memory service
memory_service = InMemoryMemoryService()

# Step 2: Provide BOTH services to runner
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service,  # For conversations
    memory_service=memory_service  # For long-term knowledge
)
```

### DO: Transfer Sessions to Memory

```python
# Manual approach
session = await session_service.get_session(
    app_name="my_app",
    user_id="user123",
    session_id="convo_01"
)

await memory_service.add_session_to_memory(session)
```

**When to transfer:**
- After each conversation turn (real-time updates)
- At end of conversation (batch processing)
- Periodically for long conversations

### DO: Choose the Right Memory Retrieval Pattern

```python
# Reactive: Agent decides when to search
agent = LlmAgent(
    instruction="Use load_memory when you need past information",
    tools=[load_memory]
)

# Proactive: Always search before responding
agent = LlmAgent(
    instruction="Answer using any relevant memories",
    tools=[preload_memory]
)
```

**load_memory vs preload_memory:**

| Pattern | When Agent Searches | Token Usage | Best For |
|---------|-------------------|-------------|----------|
| `load_memory` | Only when agent decides | Lower (searches on demand) | Specific recall needs |
| `preload_memory` | Before every turn | Higher (always searches) | Guaranteed context |

### DO: Search Memory Programmatically

```python
# Search for specific information
search_response = await memory_service.search_memory(
    app_name="my_app",
    user_id="user123",
    query="user's favorite color"
)

for memory in search_response.memories:
    print(f"{memory.author}: {memory.content.parts[0].text}")
```

### DO: Understand Memory Consolidation

**What consolidation does:**
```
Before: 50 messages with redundancy and noise
After: 5 key facts extracted

Example:
Input:  "My favorite color is blue. Actually, I prefer blue-green. Yeah, blue-green is best."
Output: Memory { favorite_color: "blue-green" }
```

**Implementation:**
- **InMemoryMemoryService**: Stores all events (no consolidation)
- **VertexAiMemoryBankService**: Automatic LLM-powered consolidation

### DON'T: Expect Semantic Search with InMemoryMemoryService

```python
# InMemoryMemoryService uses keyword matching
search_response = await memory_service.search_memory(
    query="preferred hue"  # Won't match "favorite color" - different keywords!
)

# For semantic search, use VertexAiMemoryBankService
# "preferred hue" WILL match "favorite color" (understands meaning)
```

## Callbacks

### DO: Use Callbacks for Automation

```python
async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    after_agent_callback=auto_save_to_memory
)
```

### DO: Understand Callback Types

```python
agent = LlmAgent(
    before_agent_callback=log_request,  # Before agent processes request
    after_agent_callback=auto_save_to_memory,  # After agent responds
    before_tool_callback=validate_tool_input,  # Before tool execution
    after_tool_callback=log_tool_result,  # After tool execution
    on_model_error_callback=handle_llm_error  # On LLM errors
)
```

### DO: Access Context in Callbacks

```python
async def my_callback(callback_context):
    # Access session
    session = callback_context._invocation_context.session

    # Access memory service
    memory_service = callback_context._invocation_context.memory_service

    # Access agent state
    agent_name = callback_context._invocation_context.agent.name
```

### DON'T: Block in Callbacks

```python
# Bad: Synchronous blocking operation
def blocking_callback(callback_context):
    time.sleep(5)  # Blocks entire agent execution!

# Good: Async non-blocking
async def async_callback(callback_context):
    await asyncio.sleep(5)  # Doesn't block
```

## Runner and Session Management

### DO: Use run_debug() for Prototyping
```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Your query here")
```

**Note:** `run_debug()` abstracts session creation and maintenance for quick prototyping.

### DO: Use InMemoryRunner for Basic Workflows
```python
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=root_agent)
```

## Development and Debugging

### DO: Test Incrementally
1. Test individual agents first
2. Verify state passing between agents
3. Test the complete workflow
4. Use ADK web UI for detailed traces

### DO: Use ADK Web Interface for Debugging
The web interface provides detailed traces of agent thoughts and actions, making it easier to understand and debug agent behavior.

## Observability and Evaluation

### DO: Use Logging for Development Debugging
```bash
# Start ADK web UI with DEBUG logging
adk web --log_level DEBUG
```

### DO: Implement Production Observability with Plugins
```python
from google.adk.plugins import BasePlugin

class LoggingPlugin(BasePlugin):
    def before_agent(self, callback_context):
        print(f"Agent invoked: {callback_context._invocation_context.agent.name}")

    def after_tool(self, callback_context):
        print(f"Tool executed: {callback_context.tool_name}")

# Register plugin once on Runner
runner = Runner(agent=agent, plugins=[LoggingPlugin()])
```

### DO: Create Comprehensive Evaluation Sets
```python
# Create test_config.json
{
    "criteria": {
        "tool_trajectory_avg_score": 1.0,  # Perfect tool usage
        "response_match_score": 0.8  # 80% similarity
    }
}

# Run evaluation
!adk eval agent_dir evalset.json --config_file_path=test_config.json
```

### DON'T: Skip Regression Testing
- Always run evaluations after code changes
- Track evaluation history over time
- Integrate into CI/CD pipelines

## Agent2Agent Communication

### DO: Use A2A for Cross-Organization Integration
```python
# Expose agent via A2A
from google.adk.a2a.utils.agent_to_a2a import to_a2a

a2a_app = to_a2a(my_agent, port=8001)
# Serves agent card at /.well-known/agent-card.json
```

### DO: Consume Remote Agents
```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

remote_agent = RemoteA2aAgent(
    name="external_service",
    agent_card="https://vendor.com/.well-known/agent-card.json"
)

# Use as sub-agent
main_agent = LlmAgent(
    sub_agents=[remote_agent]
)
```

### DON'T: Use A2A for Same-Process Agents
- Use local sub-agents for agents in the same codebase
- A2A is for cross-organization, cross-language, or cross-framework scenarios
- Local sub-agents are faster and simpler

## Production Deployment

### DO: Deploy to Vertex AI Agent Engine
```python
# Create requirements.txt
google-adk

# Create .env
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI=1

# Create .agent_engine_config.json
{
    "min_instances": 0,  # Scale to zero
    "max_instances": 1,
    "resource_limits": {"cpu": "1", "memory": "1Gi"}
}

# Deploy
!adk deploy agent_engine --project=PROJECT_ID --region=us-west1 agent_dir
```

### DO: Enable Memory Bank for Production
```python
from google.adk.tools.built_in_tools import PreloadMemoryTool

agent = LlmAgent(
    tools=[PreloadMemoryTool()]  # Auto-loads memories before each turn
)
```

### DON'T: Forget to Clean Up Test Deployments
```python
# Delete deployment to avoid costs
agent_engines.delete(resource_name=agent.resource_name, force=True)
```

## Common Pitfalls to Avoid

### Avoid QPM (Queries Per Minute) Limits
- Don't use "Run all cells" in notebooks
- Run cells one at a time in order
- Be mindful of API rate limits

### Avoid Unclear Agent Roles
- Each agent should have a single, well-defined purpose
- Don't create agents with overlapping responsibilities

### Avoid Over-Reliance on LLM Orchestration
- For predictable workflows, use SequentialAgent
- Only use LLM orchestration when dynamic decisions are truly needed
- LLM-based coordination can be unpredictable

### Avoid Confusing Sessions and Memory
- Sessions = Short-term conversation tracking (single conversation)
- Memory = Long-term knowledge storage (across conversations)
- Don't expect session data to be automatically available in memory
- Must explicitly transfer: `await memory_service.add_session_to_memory(session)`

### Avoid Forgetting to Enable Memory Retrieval
- Adding `memory_service` to Runner isn't enough
- Agent needs memory tools: `load_memory` or `preload_memory`
- Without these tools, agent can't access stored memories

### Avoid Manual State Management at Scale
- Session state works for simple data
- For complex knowledge, use Memory with consolidation
- Managed services (Vertex AI) automate extraction and deduplication
