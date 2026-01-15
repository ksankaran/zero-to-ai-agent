# From: Zero to AI Agent, Chapter 12, Section 12.1
# File: exercise_2_12_1_solution.md

## Exercise 2 Solution: Trace the Tool Flow

Here's the complete flow for the conversation:

**Step 1**: User sends message with two requests
- Input: "Search for information about LangChain and calculate 15% of 2000"

**Step 2**: AI parses and recognizes two distinct tasks
- Task A: Search for LangChain information (needs search tool)
- Task B: Calculate 15% of 2000 (needs calculator tool)

**Step 3**: AI decides tool execution order
- Likely executes search first (more complex, takes longer)
- Plans to execute calculator second

**Step 4**: First tool execution - Search
- Tool call: `search_tool("LangChain")`
- Tool returns: Information about LangChain framework, Harrison Chase, etc.

**Step 5**: Second tool execution - Calculator
- Tool call: `calculator_tool("0.15 * 2000")` or `calculator_tool("2000 * 0.15")`
- Tool returns: "300"

**Step 6**: AI processes both results
- Formats search results into coherent paragraph
- Formats calculation result into clear statement

**Step 7**: AI combines results into single response
- Structures response with both answers
- Maintains conversational flow
- Returns complete answer to user

**Key Insights**:
- AI can recognize multiple tasks in one request
- Tools can be executed sequentially
- Results are combined intelligently
- The AI maintains context throughout
