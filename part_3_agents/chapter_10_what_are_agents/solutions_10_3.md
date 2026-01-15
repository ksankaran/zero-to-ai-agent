# Chapter 10, Section 10.3: The Agent Loop Concept - Exercise Solutions

## Exercise 1 Solution: Loop Stage Identification

1. **Checking if a file exists before trying to read it**
   - **Stage:** OBSERVE
   - **Explanation:** Gathering information about current state

2. **Deciding to use a web search tool for current information**
   - **Stage:** THINK
   - **Explanation:** Making a decision about which action to take

3. **Calling an API to get weather data**
   - **Stage:** ACT
   - **Explanation:** Executing the chosen action

4. **Noting that the last approach didn't work**
   - **Stage:** REFLECT
   - **Explanation:** Evaluating the result of a previous action

5. **Updating memory with a new user preference discovered during conversation**
   - **Stage:** LEARN
   - **Explanation:** Storing information for future use

6. **Reading the user's question at the start**
   - **Stage:** OBSERVE
   - **Explanation:** Initial observation to understand the task

## Exercise 2 Solution: Loop Design Challenge - Pizza Ordering

**Task:** Order pizza for the office party

**Loop Design:**

**Iteration 1: Gather Requirements**
- Trigger: Initial request received
- Observe: User wants pizza for office party
- Think: Need basic information about the event
- Act: Ask for number of attendees
- State tracked: Goal set, status = "gathering_info"
- Continue: Yes, need more information

**Iteration 2: Calculate Quantity**
- Trigger: User provides "20 people"
- Observe: 20 people attending
- Think: Calculate 3 slices per person = 60 slices = 8 pizzas
- Act: Ask about dietary restrictions
- State tracked: attendee_count = 20, pizzas_needed = 8
- Continue: Yes, need dietary info

**Iteration 3: Handle Dietary Needs**
- Trigger: User mentions "2 vegetarians, 1 vegan, 1 gluten-free"
- Observe: Multiple dietary restrictions
- Think: Need variety - regular, vegetarian, vegan, gluten-free options
- Act: Ask about budget
- State tracked: dietary_restrictions recorded
- Continue: Yes, need budget info

**Iteration 4: Budget Check**
- Trigger: User provides "$200 budget"
- Observe: $200 for 8 pizzas = $25 per pizza maximum
- Think: Budget is reasonable for standard pizzas
- Act: Search for restaurants that accommodate all needs
- State tracked: budget = 200, per_pizza_max = 25
- Continue: Yes, need to find restaurant

**Iteration 5: Restaurant Selection**
- Trigger: Search results returned
- Observe: Found 3 suitable restaurants
- Think: Compare prices, reviews, and availability
- Act: Check delivery times for party time
- State tracked: restaurant_options identified
- Continue: Yes, need to confirm availability

**Iteration 6: Create Order**
- Trigger: Tony's Pizza can deliver at party time
- Observe: Restaurant selected, all requirements met
- Think: Distribute pizza types to accommodate everyone
- Act: Create order - 4 regular, 2 vegetarian, 1 vegan, 1 gluten-free
- State tracked: order composition determined
- Continue: Yes, need to place order

**Iteration 7: Place Order**
- Trigger: Order details ready
- Observe: Total cost $185, within budget
- Think: Everything checks out
- Act: Place order and get confirmation number
- State tracked: order placed, confirmation received
- Continue: Yes, need to notify

**Iteration 8: Complete Task**
- Trigger: Order confirmed
- Observe: Order successfully placed
- Think: Should inform relevant people
- Act: Send confirmation email to party organizer
- State tracked: notifications sent
- Continue: No - task complete!

**Common Problems Handled:**
- **Restaurant closed:** Return to restaurant search, mark as unavailable
- **Over budget:** Recalculate quantities, adjust specialty pizzas
- **Items unavailable:** Check alternatives, update options
- **Delivery conflict:** Try next restaurant option

**Loop Ends When:**
- Order successfully placed (primary success)
- Max iterations reached (safety limit)
- No restaurants meet requirements (failure case)
- User cancels (external termination)

## Exercise 3 Solution: Loop Problem Diagnosis

**Agent Task:** Schedule a meeting with all team members

**Problems and Solutions:**

1. **Keeps asking for team member names even after being told**
   - **Cause:** State not properly maintained between iterations
   - **Fix:** Ensure state.team_members list persists across iterations, implement proper state management

2. **Checks the same calendar repeatedly**
   - **Cause:** Not tracking which calendars have been checked
   - **Fix:** Add state.checked_calendars set to avoid redundant checks, mark calendars as processed

3. **Never actually sends the meeting invite**
   - **Cause:** Missing completion action or incorrect stopping condition
   - **Fix:** Add explicit 'send_invite' action when suitable time found, ensure completion triggers properly

4. **Eventually times out after 50 iterations**
   - **Cause:** No progress being made, stuck in loop without advancement
   - **Fix:** Add progress tracking, implement early exit if no progress for 5 iterations, add backtracking capability

**Root Cause Analysis:**
The core issue is poor state management. The agent isn't properly tracking what it has done, what it knows, and what remains to be done. This leads to repetitive actions and inability to complete the task.

**Comprehensive Fix:**
- Implement proper state object with: team_members[], checked_calendars{}, suitable_times[], progress_counter
- Add progress validation after each iteration
- Include explicit completion actions in the loop
- Set reasonable iteration limits with meaningful exit conditions
