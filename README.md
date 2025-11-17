# Momentum - personal Wellness Coach

An AI-powered wellness coach built with Google's Agent Development Kit (ADK). Momentum helps users plan, track, and optimize their fitness and nutrition goals through intelligent conversation and adaptive recommendations.

## Project Overview

This project implements a comprehensive wellness coaching system using a hub-and-spoke agent architecture with the following capabilities:

- **Personalized Planning**: Generates customized workout plans based on user goals and preferences
- **Exercise Instruction**: Provides detailed how-to guides and video resources for exercises
- **Progress Tracking**: Logs workouts and nutrition with detailed performance metrics
- **Adaptive Coaching**: Learns from user feedback to adjust plans dynamically
- **Calendar Integration**: Schedules workouts directly to Google Calendar
- **Nutrition Analysis**: Tracks meals and provides macro-nutrient summaries
- **Safety-First**: Implements critic loops to ensure safe progression rates

## Technology Stack

- **Google Agent Development Kit (ADK)**: Agent orchestration and LLM integration
- **Firestore**: Long-term memory and data persistence
- **Google Calendar API**: Workout scheduling via MCP
- **Nutritionix API**: Nutrition data and macro calculations
- **Code Execution**: Data analysis and aggregation

## Development Approach

This project follows an incremental, phase-based development approach with 11 distinct phases, each building on the previous one. Each phase delivers a working, demo-able feature set.

See [docs/roadmap.md](docs/roadmap.md) for the complete development roadmap.

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
   adk web --log_level DEBUG
   ```

   The web interface will be available at `http://localhost:8000`

For phase-specific setup instructions, see `docs/phases/phase-{N}.md`.

## Current Status

🚀 **Phase**: Phase 0 - Project Setup (Complete)
📝 **Next**: Phase 1 - Chat-Planner (MVA)

See [docs/PROGRESS.md](docs/PROGRESS.md) for detailed progress tracking.

## License

This project is part of the Kaggle 5-Day AI Agents Intensive Course Capstone Project.
