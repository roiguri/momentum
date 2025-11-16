# AI Agents Development Checklist

## Agent Design Fundamentals

### Single Agent vs Multi-Agent Decision
- [ ] Evaluate if a single agent can handle the task or if specialization is needed
- [ ] Consider if the task is complex enough to warrant multiple specialized agents
- [ ] Avoid creating monolithic "do-it-all" agents for complex tasks
- [ ] Prefer multi-agent systems for better maintainability, debugging, and reliability

### Agent Configuration
- [ ] Define clear `name` and `description` for agent identification
- [ ] Specify the appropriate `model` (e.g., gemini-2.5-flash-lite)
- [ ] Write clear and specific `instruction` prompts that define the agent's goal and behavior
- [ ] Assign appropriate `tools` that the agent needs to complete its tasks
- [ ] Set `output_key` for agents that need to share state with other agents

## Multi-Agent System Architecture

### Agent Specialization
- [ ] Ensure each agent has one clear, focused responsibility
- [ ] Make agents simple and specialized rather than complex and general-purpose
- [ ] Design agents to be independently testable

### Workflow Pattern Selection
- [ ] **Sequential**: Use when order matters and each step builds on the previous one
- [ ] **Parallel**: Use when tasks are independent and can execute concurrently for speed
- [ ] **Loop**: Use when iterative refinement and quality improvement is needed
- [ ] **LLM-based Orchestration**: Use when dynamic decision-making is required

### State Management
- [ ] Use `output_key` to store agent results in session state
- [ ] Use placeholders (e.g., `{research_findings}`) to inject state values into agent instructions
- [ ] Ensure data flows correctly between agents in sequential workflows
- [ ] Plan how parallel agents will aggregate their results

## Error Handling and Reliability

### Retry Configuration
- [ ] Configure retry options for LLM calls to handle transient errors
- [ ] Set appropriate `attempts` (e.g., 5 maximum retry attempts)
- [ ] Configure `exp_base` for exponential backoff delay
- [ ] Set `initial_delay` before first retry
- [ ] Specify `http_status_codes` to retry on (e.g., 429, 500, 503, 504)

## Tool Integration

### Tool Type Selection
- [ ] Choose the appropriate tool type for your use case:
  - **Function Tools**: For custom Python functions
  - **Agent Tools**: For using other agents as tools
  - **MCP Tools**: For external services via Model Context Protocol
  - **Built-in Tools**: For pre-built capabilities (google_search, code execution)
  - **Long-Running Tools**: For operations requiring human approval or external events

### Custom Function Tools
- [ ] Follow best practices when creating custom tools:
  - Use dictionary returns with `status` field
  - Include clear docstrings (LLMs use these to understand tool purpose)
  - Add type hints for all parameters
  - Implement structured error handling
- [ ] Return structured responses: `{"status": "success", "data": ...}` or `{"status": "error", "error_message": ...}`
- [ ] Wrap Python functions in `FunctionTool` to make them callable by agents

### Agent Tools
- [ ] Wrap sub-agents in `AgentTool` to make them callable by parent agents
- [ ] Understand Agent Tools vs Sub-Agents:
  - Agent Tools: Agent A calls Agent B as a tool, B's response goes back to A
  - Sub-Agents: Agent A transfers control completely to Agent B
- [ ] Use Agent Tools for delegation (e.g., calculation specialists)
- [ ] Reference tool function names exactly in agent instructions

### MCP (Model Context Protocol) Tools
- [ ] Identify if an MCP server exists for your use case before building custom integration
- [ ] Configure `McpToolset` with appropriate connection parameters
- [ ] Use `tool_filter` to select only needed tools from MCP servers
- [ ] Handle MCP server timeout configuration appropriately

### Code Execution Tools
- [ ] Use `BuiltInCodeExecutor` for reliable calculations instead of LLM arithmetic
- [ ] Instruct agents to generate Python code for complex calculations
- [ ] Create specialist calculation agents when math reliability is critical

### Long-Running Operations
- [ ] Identify operations that need human approval or external events
- [ ] Use `ToolContext` parameter in tool functions
- [ ] Implement pause logic with `tool_context.request_confirmation()`
- [ ] Check approval status with `tool_context.tool_confirmation`
- [ ] Wrap agent in `App` with `ResumabilityConfig(is_resumable=True)`
- [ ] Handle `adk_request_confirmation` events in workflow
- [ ] Save and use `invocation_id` for resuming paused operations

### Tool Instructions
- [ ] Clearly specify in instructions when and how to use tools
- [ ] Reference tools by their exact function names in instructions
- [ ] Provide guidance on using search tools for current information
- [ ] Define exit conditions when using loop control tools
- [ ] Instruct agents to check `status` field in tool responses for errors

## Quality and Testing

### Instructions Quality
- [ ] Write clear and specific instructions that guide agent behavior
- [ ] Include output format requirements (e.g., "as a bulleted list")
- [ ] Define success criteria and exit conditions
- [ ] Avoid ambiguous or overly complex instructions

### Debugging and Observability
- [ ] Use `runner.run_debug()` for prototyping and testing
- [ ] Leverage ADK web UI for detailed traces of agent thoughts and actions
- [ ] Test individual agents before integrating them into workflows
- [ ] Verify state passing between agents works correctly

## Loop Agent Specific Considerations

### Loop Control
- [ ] Set `max_iterations` to prevent infinite loops
- [ ] Create explicit exit conditions (e.g., "APPROVED" signal)
- [ ] Design a function for loop termination (e.g., `exit_loop()`)
- [ ] Create a refiner/decision agent that can call the exit function
- [ ] Ensure the agent can distinguish between "continue refining" and "exit loop" signals

### Iterative Refinement Pattern
- [ ] Have a critic/reviewer agent provide feedback
- [ ] Have a refiner agent that incorporates feedback or triggers exit
- [ ] Use clear approval signals (e.g., exact phrase "APPROVED")
- [ ] Overwrite state with refined versions using the same `output_key`

## Session and State Management

### Session Service Selection
- [ ] Choose appropriate SessionService for your needs:
  - **InMemorySessionService**: For development/testing (temporary storage)
  - **DatabaseSessionService**: For persistent storage (survives restarts)
  - **Vertex AI Agent Engine**: For production at scale
- [ ] Provide SessionService to Runner during initialization
- [ ] Create sessions with unique session_id for each conversation thread
- [ ] Understand that sessions are isolated (don't share data between sessions)

### Session Configuration
- [ ] Create sessions with: app_name, user_id, and session_id
- [ ] Use `InMemoryRunner` for basic workflows
- [ ] Use `Runner` with SessionService for stateful conversations
- [ ] Implement `run_async()` for production workflows with event handling

### Session Events
- [ ] Understand that Events are the building blocks of conversations
- [ ] Know that Events include: user input, agent responses, tool calls, tool outputs
- [ ] Use events to track conversation flow and debug agent behavior
- [ ] Handle events appropriately in async workflows

### Session State
- [ ] Use `session.state` as a scratchpad for dynamic conversation data
- [ ] Access state via `tool_context.state` in tools
- [ ] Use descriptive key prefixes: `user:`, `app:`, `temp:`
- [ ] Understand state persists within a session but not across sessions
- [ ] Create tools to manage session state (save/retrieve patterns)

### Context Management
- [ ] Implement context compaction to manage long conversations
- [ ] Configure `EventsCompactionConfig` with:
  - `compaction_interval`: When to trigger compaction
  - `overlap_size`: How much previous context to retain
- [ ] Wrap agent in `App` to enable context compaction features
- [ ] Understand compaction creates summary events to replace verbose history
- [ ] Consider custom compaction strategies for specialized use cases

### Context Optimization
- [ ] Use context caching to reduce token usage for static instructions
- [ ] Monitor conversation length and trigger compaction appropriately
- [ ] Balance between context retention and token cost
- [ ] Test compaction settings with realistic conversation flows

## Memory Management

### Memory Service Selection
- [ ] Choose appropriate MemoryService:
  - **InMemoryMemoryService**: For prototyping (keyword matching, no persistence)
  - **VertexAiMemoryBankService**: For production (semantic search, LLM consolidation)
- [ ] Provide both SessionService and MemoryService to Runner
- [ ] Understand Memory provides long-term knowledge across sessions

### Memory Integration Workflow
- [ ] **Initialize**: Create MemoryService and provide to Runner
- [ ] **Ingest**: Transfer session data using `add_session_to_memory()`
- [ ] **Retrieve**: Search memories using `search_memory()` or agent tools

### Memory Storage
- [ ] Manually save sessions: `await memory_service.add_session_to_memory(session)`
- [ ] Automate saving with `after_agent_callback`
- [ ] Decide when to save: after each turn, end of conversation, or periodic intervals
- [ ] Verify data is stored by searching memories

### Memory Retrieval
- [ ] Choose retrieval strategy:
  - **load_memory**: Reactive (agent decides when to search)
  - **preload_memory**: Proactive (always loads before each turn)
- [ ] Add memory tools to agent's tools array
- [ ] Instruct agent on when/how to use memory tools
- [ ] Test retrieval across different sessions

### Memory Search
- [ ] Use `search_memory()` for manual searches in code
- [ ] Understand search behavior:
  - InMemoryMemoryService: Keyword matching
  - VertexAiMemoryBankService: Semantic/meaning-based
- [ ] Craft effective search queries
- [ ] Process SearchMemoryResponse results appropriately

### Memory Consolidation
- [ ] Understand consolidation extracts key facts from verbose conversations
- [ ] Know that managed services (Vertex AI) handle consolidation automatically
- [ ] Design conversations to facilitate fact extraction
- [ ] Test that important information is being consolidated correctly

## Callbacks and Event Handling

### Callback Configuration
- [ ] Understand callback types:
  - `before_agent_callback` / `after_agent_callback`
  - `before_tool_callback` / `after_tool_callback`
  - `before_model_callback` / `after_model_callback`
  - `on_model_error_callback`
- [ ] Use callbacks for logging, observability, and automation
- [ ] Access runtime context via `callback_context` parameter
- [ ] Implement async callbacks for I/O operations

### Common Callback Patterns
- [ ] Automatic memory storage with `after_agent_callback`
- [ ] Logging and monitoring with before/after callbacks
- [ ] Custom validation with tool callbacks
- [ ] Error handling and recovery with error callbacks

## Observability and Debugging

### Logging Configuration
- [ ] Use `--log_level DEBUG` with `adk web` for development debugging
- [ ] Configure Python logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Use LoggingPlugin for production observability
- [ ] Understand the three pillars: Logs (what), Traces (why), Metrics (how well)

### Development Debugging
- [ ] Use ADK web UI to inspect agent behavior and tool calls
- [ ] Examine Events tab for chronological action lists
- [ ] Use Trace view for timing information and performance analysis
- [ ] Inspect function calls and LLM requests/responses in DEBUG logs

### Production Observability
- [ ] Implement LoggingPlugin for automated logging across all agents
- [ ] Create custom plugins for specialized logging needs
- [ ] Use plugins to track agent invocations, tool calls, and LLM requests
- [ ] Implement callbacks within plugins for logging, monitoring, and analytics

### Plugin Development
- [ ] Understand plugins are composed of callbacks
- [ ] Register plugins once on Runner to apply to all agents
- [ ] Use BasePlugin as foundation for custom plugins
- [ ] Implement appropriate callback hooks for your monitoring needs

## Agent Evaluation and Testing

### Evaluation Strategy
- [ ] Create evaluation sets (*.evalset.json) with test cases
- [ ] Define evaluation criteria in test_config.json
- [ ] Set appropriate thresholds for tool_trajectory_avg_score and response_match_score
- [ ] Run evaluations using `adk eval` CLI or pytest

### Test Case Creation
- [ ] Save conversations from ADK web UI as test cases
- [ ] Create synthetic test cases for edge cases
- [ ] Include user_content, final_response, and intermediate_data (tool_uses)
- [ ] Organize test cases by scenario (basic, edge cases, error handling)

### Evaluation Metrics
- [ ] Tool Trajectory Score: Measures correct tool usage and parameters
- [ ] Response Match Score: Measures text similarity to expected response
- [ ] Set score thresholds based on requirements (e.g., 1.0 for perfect tool usage)
- [ ] Analyze failures to understand root causes

### Regression Testing
- [ ] Run evaluations after code changes to detect regressions
- [ ] Use `--print_detailed_results` flag for debugging failures
- [ ] Track evaluation history over time
- [ ] Integrate evaluation into CI/CD pipelines

### Advanced Evaluation
- [ ] Consider User Simulation for dynamic testing
- [ ] Test with varied, unpredictable user inputs
- [ ] Use ConversationScenario for goal-oriented testing
- [ ] Leverage LLM-generated prompts for comprehensive coverage

## Agent2Agent Communication

### A2A Protocol Decision
- [ ] Use A2A when agents are in different codebases or organizations
- [ ] Use A2A for cross-language/framework communication
- [ ] Use A2A when formal contracts are needed between services
- [ ] Use local sub-agents for same-process, internal agent communication

### Exposing Agents via A2A
- [ ] Use `to_a2a()` to expose agent as A2A-compatible service
- [ ] Ensure agent card is served at `/.well-known/agent-card.json`
- [ ] Deploy agent with appropriate port configuration
- [ ] Document agent capabilities in agent card

### Consuming Remote Agents
- [ ] Use `RemoteA2aAgent` to create client-side proxy
- [ ] Point to remote agent's agent card URL
- [ ] Use remote agent as sub-agent in agent tools array
- [ ] Handle network errors and retries appropriately

### A2A Architecture Patterns
- [ ] Cross-Framework: ADK agent calling agents in other frameworks
- [ ] Cross-Language: Python agent calling Java/Node.js agents
- [ ] Cross-Organization: Internal agents consuming external vendor services
- [ ] Understand A2A protocol communication (HTTP POST to /tasks endpoint)

## Production Deployment

### Deployment Platform Selection
- [ ] Choose Vertex AI Agent Engine for managed, auto-scaling deployments
- [ ] Consider Cloud Run for serverless, easy-to-start deployments
- [ ] Use GKE for full control over containerized multi-agent systems
- [ ] Evaluate based on scale, complexity, and operational requirements

### Agent Engine Deployment
- [ ] Create requirements.txt with dependencies
- [ ] Configure .env with GOOGLE_CLOUD_LOCATION and backend settings
- [ ] Create .agent_engine_config.json for resource limits and scaling
- [ ] Use `adk deploy agent_engine` CLI command

### Deployment Configuration
- [ ] Set min_instances and max_instances for auto-scaling
- [ ] Configure CPU and memory resource limits
- [ ] Choose appropriate deployment region for latency and compliance
- [ ] Enable tracing for production debugging

### Production Memory Management
- [ ] Use Vertex AI Memory Bank for long-term cross-session memory
- [ ] Add PreloadMemoryTool or LoadMemoryTool to agent
- [ ] Configure callbacks to save conversations to Memory Bank
- [ ] Understand semantic search capabilities vs keyword matching

### Cost Management
- [ ] Delete test deployments promptly to avoid charges
- [ ] Use min_instances=0 for scale-to-zero when idle
- [ ] Monitor usage via Vertex AI Console
- [ ] Understand free tier limits and pricing structure

### Monitoring and Management
- [ ] Monitor deployed agents via Vertex AI Console
- [ ] Use Cloud Logging for production log analysis
- [ ] Enable Cloud Trace for performance monitoring
- [ ] Implement health checks and alerting
