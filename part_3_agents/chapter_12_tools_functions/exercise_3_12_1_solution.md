# From: Zero to AI Agent, Chapter 12, Section 12.1
# File: exercise_3_12_1_solution.md

## Exercise 3 Solution: Design a Tool Set for a Bakery

Here are 5 essential tools for a bakery AI assistant:

**Tool 1: order_manager**
- **Purpose**: Create, view, and update customer orders
- **When used**: "Add a birthday cake order for Saturday" or "What orders do we have for tomorrow?"
- **Inputs**: Action (create/read/update), order details (customer, items, date, special requests)
- **Outputs**: Order confirmation or list of orders with details
- **Safety**: Validate dates are future dates, check item availability, require customer contact info

**Tool 2: recipe_calculator**
- **Purpose**: Scale recipes up or down based on needed quantities
- **When used**: "How much flour do I need to make 5 dozen cookies?" or "Scale the bread recipe for 20 loaves"
- **Inputs**: Recipe name, desired quantity, unit (dozens, loaves, etc.)
- **Outputs**: Adjusted ingredient list with precise measurements
- **Safety**: Validate recipe exists, check for reasonable quantities (not 10,000 cookies), warn about oven capacity

**Tool 3: price_calculator**
- **Purpose**: Calculate prices for custom orders including ingredients, labor, and markup
- **When used**: "How much should we charge for a 3-tier wedding cake?" or "What's the cost breakdown for 100 cupcakes?"
- **Inputs**: Item type, quantity, special requirements (decorations, delivery, etc.)
- **Outputs**: Itemized cost breakdown and suggested retail price
- **Safety**: Ensure minimum price thresholds, validate against pricing rules, flag unusual requests

**Tool 4: supplier_contact**
- **Purpose**: Check supplier prices, availability, and place ingredient orders
- **When used**: "Order more vanilla extract" or "Check flour prices from our suppliers"
- **Inputs**: Ingredient name, quantity needed, urgency level
- **Outputs**: Supplier options with prices, availability, and order confirmation
- **Safety**: Require approval for orders over certain amount, verify supplier is approved, check budget limits

**Tool 5: daily_prep_list**
- **Purpose**: Generate preparation schedule based on orders and recipes
- **When used**: "What needs to be started tonight for tomorrow?" or "Create tomorrow's baking schedule"
- **Inputs**: Date, available staff, oven capacity
- **Outputs**: Time-based task list with priorities and assigned stations
- **Safety**: Check for conflicts, ensure critical items are prioritized, validate against operating hours

**Bonus Tool 6: allergy_checker**
- **Purpose**: Verify ingredients against customer allergies and dietary restrictions
- **When used**: "Can we make this gluten-free?" or "Check if the chocolate cake is nut-free"
- **Inputs**: Recipe or item name, dietary restrictions
- **Outputs**: Safe/unsafe determination with specific ingredients of concern
- **Safety**: Always err on side of caution, include disclaimer about cross-contamination

These tools transform the AI from a chatbot into a true bakery operations assistant!
