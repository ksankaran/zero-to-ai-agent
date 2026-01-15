# Chapter 10, Section 10.2: Agent Components - Exercise Solutions

## Exercise 1 Solution: Component Identification

1. **Remembering that a user prefers morning meetings**
   - **Component:** MEMORY (Long-term/semantic memory)
   - **Explanation:** Stores user preferences for future use

2. **Deciding to check weather before suggesting outdoor activities**
   - **Component:** REASONING
   - **Explanation:** Logical decision-making based on context

3. **Using a calculator to split a restaurant bill**
   - **Component:** TOOLS
   - **Explanation:** Direct tool execution for a specific task

4. **Learning from a failed attempt and trying a different approach**
   - **Components:** MEMORY + REASONING + TOOLS
   - **Explanation:** Memory stores what didn't work, Reasoning analyzes why and devises new approach, Tools execute new approach

5. **Knowing which API to call for stock prices**
   - **Components:** REASONING + MEMORY
   - **Explanation:** Reasoning determines need for stock data, Memory knows which tool provides that capability

6. **Maintaining conversation context across multiple turns**
   - **Component:** MEMORY (Short-term/working memory)
   - **Explanation:** Keeps track of conversation state and history

## Exercise 2 Solution: Design Challenge - Meal Planning Agent

**Reasoning Patterns:**
- Primary: Plan-and-Execute (for weekly meal planning)
- Secondary: ReAct (for adapting to constraints and availability)
- Fallback: Reflexion (for improving based on user feedback)

**Tools Needed:**
- Recipe database API (search recipes by criteria)
- Nutrition calculator (ensure balanced meals)
- Price checker (get current ingredient prices)
- Calendar integration (check for special events)
- Shopping list generator (organize by store sections)
- Meal prep scheduler (optimize cooking time)
- Ingredient substitution tool (handle allergies/preferences)

**Memory Types:**
- **User Preferences:** Dietary restrictions, favorite cuisines, disliked ingredients
- **Meal History:** Recent meals (avoid repetition), ratings, frequency tracking
- **Pantry State:** Available ingredients, shopping needs
- **Budget Tracking:** Weekly spending, average meal costs

**Handling Scenarios:**
- **Dietary Restrictions:** Filter all recipes through restriction checker first
- **Budget Constraints:** Calculate total cost before finalizing, suggest alternatives if over
- **Previous Meals:** Check last 14 days to ensure variety
- **Ingredient Availability:** Check pantry first, only add missing items to shopping list

## Exercise 3 Solution: Component Interaction Mapping

**Task:** "Book a flight to Seattle for my conference"

**1. What Reasoning Determines First:**
- Parse request: destination (Seattle), purpose (conference)
- Identify missing information: dates, departure city, preferences
- Plan sequence: get details → search flights → select best → book

**2. Relevant Memory:**
- User's home airport (from previous bookings)
- Preferred airlines and seat preferences
- Typical travel class for business trips
- Conference dates (if mentioned previously)
- Company travel policies
- Past booking patterns

**3. Tool Sequence Needed:**
1. Calendar tool → Get conference dates
2. Flight search API → Find available flights
3. Price comparison tool → Evaluate options
4. Seat selector → Check preferred seats
5. Booking API → Complete reservation
6. Calendar update → Add flight details
7. Email sender → Send confirmation

**4. Handling Complications:**

**Sold Out Preferred Flight:**
- TOOLS detect preferred morning flight unavailable
- REASONING evaluates alternatives
- MEMORY recalls user once took afternoon flight successfully
- TOOLS search wider time window
- Resolution: Book alternative with explanation

**Price Exceeds Policy:**
- TOOLS find all options exceed budget
- REASONING considers approval or date change
- MEMORY notes manager approved override before
- TOOLS check adjacent dates
- Resolution: Present options to user

**Connection Required:**
- TOOLS detect no direct flights
- REASONING evaluates connection options
- MEMORY recalls user dislikes tight connections
- TOOLS filter for 90+ minute layovers
- Resolution: Book connection with adequate layover time

**The Key Pattern:**
Each component continuously feeds information to the others. Memory informs Reasoning, which directs Tools, whose results update Memory and trigger new Reasoning. This creates an intelligent feedback loop that adapts to complications and achieves the goal.
