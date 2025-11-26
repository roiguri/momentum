# Momentum - Personal Wellness Coach

An AI-powered wellness coach built with Google's Agent Development Kit (ADK). Momentum helps users plan, track, and optimize their fitness and nutrition goals through intelligent conversation and adaptive recommendations.

## Project Overview

This project implements a comprehensive wellness coaching system using a hub-and-spoke agent architecture with the following capabilities:

### Current Features (Phases 1-4)

- ✅ **Personalized Planning**: Generates customized workout plans based on user goals, experience level, and availability
- ✅ **Exercise Instruction**: Provides context-aware exercise guidance with YouTube videos
  - Concise overview on first mention
  - Detailed breakdown on follow-up questions
  - Focused answers for specific questions
- ✅ **Persistent Sessions**: Conversations survive application restarts using SQLite
- ✅ **User Memory**: Agent remembers important facts across different conversations
- ✅ **Plan Storage**: Save and retrieve workout plans with query capabilities
  - Firestore-compatible schema for future migration

### Planned Features (Phases 5-11)

- 📋 **Progress Tracking**: Log workouts and nutrition with detailed performance metrics
- 🔄 **Adaptive Coaching**: Learn from user feedback to adjust plans dynamically
- 📅 **Calendar Integration**: Schedule workouts directly to Google Calendar
- 🥗 **Nutrition Analysis**: Track meals and provide macro-nutrient summaries
- 🛡️ **Safety-First**: Implement critic loops to ensure safe progression rates
- 🌐 **A2A Protocol**: Expose agent as a discoverable service for other AI agents

## Architecture

**Hub-and-Spoke Pattern** with specialized agents:

- **WellnessChiefAgent** (Hub): Main orchestrator for workout planning and coaching
- **InstructorAgent** (Spoke): Exercise instruction with Google Search for video resources

**Persistence Layers**:
- **Sessions**: SQLite database (`DatabaseSessionService`) for conversation history
- **Memory**: In-memory service (`InMemoryMemoryService`) for cross-session user facts
- **Plans**: File-based JSON storage with Firestore-compatible schema

## Technology Stack

- **Google Agent Development Kit (ADK)**: Agent orchestration and LLM integration
- **Gemini 2.5 Flash**: LLM for conversational intelligence
- **SQLite**: Session persistence
- **Google Search**: Exercise video discovery (via built-in tool)
- **Firestore** (planned): Long-term data persistence for workout logs and nutrition

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd momentum
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**:
   - Create a `.env.local` file in the project root
   - Add your Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - **Important**: Never commit `.env.local` (already in .gitignore)
   - **Note**: `agents/.env` is a symlink to `.env.local` (required by ADK)

5. **Run the agent**:
   ```bash
   adk web
   ```

   The web interface will be available at `http://localhost:8000`

## Usage Examples

### Generate a Workout Plan
```
User: "I want to train for a 5k race. I can train 3 days a week for 8 weeks."
Agent: [Asks clarifying questions about experience level and limitations]
Agent: [Generates personalized 8-week plan]
User: "Save this plan"
Agent: [Saves plan to persistent storage]
```

### Get Exercise Instruction
```
User: "How do I do a squat?"
Agent: [Provides concise overview with key form points and video]
User: "What are common mistakes?"
Agent: [Provides detailed breakdown with mistakes, modifications, and safety notes]
```

## Running Evaluations

The project includes automated evaluations using ADK's `AgentEvaluator` to test agent behavior against expected responses.

### Run All Tests
```bash
python -m pytest evals/test_eval.py -v
```

### Run Specific Test
```bash
python -m pytest evals/test_eval.py::test_instructor_agent -v
```

### Available Tests
- `test_instructor_agent` - Tests exercise instruction responses
- `test_session_persistence` - Tests session persistence across conversations
- `test_user_memory` - Tests user memory recall and preference tracking
- `test_plan_storage` - Tests workout plan creation and storage

### Memory Across Sessions
```
Session 1:
User: "My name is Roy and I have a knee injury"
Agent: [Acknowledges and stores information]

Session 2 (new conversation):
User: "What do you know about me?"
Agent: "Your name is Roy and you have a knee injury"
```

## Current Status

**Phase**: Phase 4 - Sessions, Memory & Plan Storage (Goals 1-3 Complete)  
**Progress**: 3/11 phases completed (27%)

### Completed Phases
- ✅ Phase 0: Project Setup
- ✅ Phase 1: Chat-Planner (MVA)
- ✅ Phase 2: Instructor (Adding a Spoke)
- ⚠️ Phase 3: Plan Persister (Skipped - replaced by ADK Memory)
- 🔄 Phase 4: Sessions, Memory & LROs (Goals 1-3 Complete, LROs deferred)

See [docs/PROGRESS.md](docs/PROGRESS.md) for detailed progress tracking and [docs/roadmap.md](docs/roadmap.md) for the complete development roadmap.

## Project Structure

```
momentum/
├── agents/
│   ├── agent.py              # Root agent configuration
│   ├── hub.py                # WellnessChiefAgent (main orchestrator)
│   ├── spokes/               # Specialized agents
│   │   └── instructor.py     # Exercise instruction agent
│   ├── prompts/              # Agent instruction prompts
│   ├── tools/                # Custom tools
│   │   └── plan_tools.py     # Plan storage tools
│   └── config.py             # Shared configuration
├── data/                     # Persistent data (gitignored)
│   ├── wellness_sessions.db  # Session history
│   └── plans/                # Saved workout plans
├── docs/                     # Documentation
│   ├── roadmap.md           # Development roadmap
│   ├── PROGRESS.md          # Progress tracking
│   └── phases/              # Phase-specific plans
└── requirements.txt         # Python dependencies
```

## Competition Context

This project is part of the **Kaggle 5-Day AI Agents Intensive Course Capstone Project** (Concierge Agents track).

**Key Concepts Demonstrated**:
- ✅ Multi-agent system (Hub-and-Spoke)
- ✅ Sessions & Memory (DatabaseSessionService, InMemoryMemoryService)
- ✅ Custom tools (plan storage)
- ✅ Built-in tools (Google Search)
- 📋 Long-Running Operations (planned)
- 📋 MCP Tools (Google Calendar - planned)
- 📋 Code Execution (nutrition analysis - planned)
- 📋 Loop agents (safety critic - planned)

## License

This project is part of the Kaggle 5-Day AI Agents Intensive Course Capstone Project.
