# Prompt Engineering Guidelines

This document tracks prompt engineering best practices and refinements for the Momentum agent system.

## Resources

### Official Google Gemini Documentation
- **Primary Guide**: [Prompt design strategies - Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- **Getting Started**: [Getting Started with Gemini - Prompt Engineering Guide](https://www.promptingguide.ai/models/gemini)
- **Workspace Guide**: [Gemini for Google Workspace Prompt Guide](https://workspace.google.com/learning/content/gemini-prompt-guide)

### Key Best Practices

1. **Clear Instructions**: Provide explicit, specific guidance through questions, tasks, or entities
2. **Few-Shot Examples**: Include examples to demonstrate desired patterns (show positives, not negatives)
3. **Contextual Information**: Supply relevant details the model needs rather than assuming background knowledge
4. **Avoid Over-Specification**: Break complex prompts into components; don't over-constrain
5. **Iterate and Experiment**: Test different phrasing, analogous tasks, and content ordering

### Framework: PTCF (Persona · Task · Context · Format)
- **Persona**: Who is the agent? (e.g., "expert wellness coach")
- **Task**: What should it do? (e.g., "generate personalized workout plans")
- **Context**: What constraints/background? (e.g., "based on user goals, experience, availability")
- **Format**: How should output look? (e.g., "structured weekly plan with progressive overload")

---

## Current Agent Prompts

### WellnessChiefAgent (`agents/prompts/wellness_chief.py`)

**Status**: Phase 1 - Initial implementation
**Model**: `gemini-2.5-flash`

#### Known Issues & Refinements Needed

1. **✅ FIXED: Hard-coded 4-week timeline** (2025-11-17)
   - **Issue**: Prompt previously mandated "4-week workout plan" regardless of user needs
   - **Fix Applied**: Added timeline question (#3) in Step 1 information gathering
   - **Changes**:
     - Now asks: "What is your target timeline or goal date?"
     - Examples provided: "4 weeks", "8-week program", "race on March 15"
     - Default to 4 weeks if not specified
     - Plan structure now says "Week 1, Week 2, ..., Week N" instead of hardcoding 4
     - Added guidance to scale progression appropriately for program length
     - Updated example interaction to show 8-week timeline

2. **Future Refinements** (track here as identified)
   - TODO: Add equipment availability questions (home gym, commercial gym, minimal equipment)
   - TODO: Consider rest day preferences (specific days off for work schedules)
   - TODO: Add intensity preference (conservative vs aggressive progression)
   - TODO: Comprehensive prompt review using PTCF framework in later phase

---

## Evaluation Criteria for Prompts

When refining prompts, evaluate against:

1. **Specificity**: Does it provide clear, actionable guidance?
2. **Flexibility**: Does it avoid unnecessary rigidity?
3. **Context**: Does it include sufficient background information?
4. **Examples**: Are few-shot examples provided where helpful?
5. **Safety**: Does it emphasize safety constraints (e.g., 10% progression rule)?
6. **User-Centric**: Does it gather necessary user preferences before generating output?

---

## Changelog

### 2025-11-17 - Phase 1 Initial Prompt & First Refinement
- Created initial WellnessChiefAgent prompt
- Identified 4-week hardcoding issue
- **FIXED**: Added flexible timeline question (#3) in information gathering
- Updated plan generation to support variable-length programs
- Added progression scaling guidance based on program duration
- Documented prompt engineering resources and best practices
- Created this tracking document for future refinements
