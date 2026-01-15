# From: Zero to AI Agent, Chapter 12, Section 12.1
# File: exercise_1_12_1_solution.md

## Exercise 1 Solution: Tool or No Tool?

Let's analyze each scenario:

1. **Write a haiku about summer**
   - **No tool needed**: LLM can handle this
   - **Why**: Creative writing task, requires language generation
   - **If tool used anyway**: Unnecessary complexity, slower response

2. **Get today's date**
   - **Tool needed**: Yes - Date/time tool
   - **Why**: Current, real-time information
   - **Tool type**: System date tool
   - **If no tool**: Would give wrong or no date

3. **Explain quantum physics**
   - **No tool needed**: LLM has this knowledge
   - **Why**: Established concept in training data
   - **If tool used**: Would just slow down the response unnecessarily

4. **Check if a file exists**
   - **Tool needed**: Yes - File system tool
   - **Why**: Needs to interact with actual file system
   - **Tool type**: File checking tool
   - **If no tool**: Cannot access file system

5. **Translate 'hello' to Spanish**
   - **No tool needed**: LLM knows common translations
   - **Why**: Basic language knowledge in training
   - **If tool used**: Overkill for such a simple translation

6. **Find the latest news about AI**
   - **Tool needed**: Yes - News search tool
   - **Why**: "Latest" indicates current information needed
   - **Tool type**: News API or web search
   - **If no tool**: Would only have information up to training cutoff

7. **Generate a business name**
   - **No tool needed**: LLM excels at creative generation
   - **Why**: Creative task requiring language skills
   - **If tool used**: No appropriate tool exists for creativity

8. **Calculate compound interest**
   - **Tool needed**: Yes - Financial calculator tool
   - **Why**: Precise financial calculations required
   - **Tool type**: Compound interest calculator
   - **If no tool**: Risk of calculation errors, especially with complex formulas

**Key Pattern**: Tools for current data and calculations, LLM for creativity and knowledge!
