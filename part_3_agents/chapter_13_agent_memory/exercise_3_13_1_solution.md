# Exercise 3 Solution: Memory Retrieval Strategy

## Scenario
**User Query**: "What restaurant should I try this weekend?"

**Challenge**: Hundreds of stored facts in long-term memory. How do we find the relevant ones?

---

## Step-by-Step Retrieval Algorithm

### Step 1: Query Analysis

```
ANALYZE the user query to identify:
  - Intent: "restaurant recommendation"
  - Time constraint: "this weekend"
  - Implicit needs: location, cuisine type, occasion, budget
  
OUTPUT:
  query_type: "recommendation"
  domain: "dining/restaurants"
  temporal: "upcoming_weekend"
  missing_context: [location, cuisine, budget, occasion, party_size]
```

**Reasoning**: Before searching memory, understand what information would be helpful. A restaurant recommendation benefits from knowing preferences, location, dietary restrictions, and past experiences.

---

### Step 2: Identify Relevant Memory Categories

```
RELEVANT_CATEGORIES = [
  "dietary_restrictions",     # CRITICAL - must not recommend unsafe food
  "food_preferences",         # Strong likes/dislikes
  "cuisine_preferences",      # Favorite cuisines
  "location",                 # Where the user lives/will be
  "budget_preferences",       # Dining budget range
  "past_restaurant_mentions", # Places they've discussed before
  "dining_companions",        # Do they usually dine with others?
  "recent_dining_experiences" # What they've tried recently
]

EXCLUDED_CATEGORIES = [
  "work_projects",
  "health_conditions",        # Unless specifically diet-related
  "financial_accounts",
  "travel_plans"              # Unless this weekend involves travel
]
```

**Reasoning**: Cast a wide net on food-related categories, but don't waste context on irrelevant domains. Dietary restrictions are highest priority due to safety implications.

---

### Step 3: Retrieval Strategy (Multi-Stage)

```
STAGE 1: Critical Safety Retrieval (Always Include)
  QUERY: category = "dietary_restrictions" OR category = "allergies"
  LIMIT: None (include ALL matches)
  RECENCY_WEIGHT: 0 (old allergies still valid)
  
  OUTPUT: ["allergic to shellfish", "vegetarian since 2023"]

STAGE 2: Semantic Search on Preferences
  QUERY: Embed("restaurant recommendation weekend dining")
  SEARCH: Vector similarity against food/dining memories
  LIMIT: Top 10 by similarity score
  THRESHOLD: similarity > 0.7
  
  OUTPUT: ["loves Italian food", "mentioned wanting to try Thai", 
           "dislikes loud restaurants", "prefers outdoor seating"]

STAGE 3: Recency-Weighted Recent Context
  QUERY: category IN ("dining", "restaurants", "food")
  FILTER: created_at > (now - 90 days)
  SORT BY: recency_score * relevance_score
  LIMIT: 5
  
  OUTPUT: ["tried Olive Garden last month - said it was just okay",
           "asked about sushi places 2 weeks ago"]

STAGE 4: Location and Logistics
  QUERY: category = "location" OR category = "transportation"
  LIMIT: 2-3 most recent
  
  OUTPUT: ["lives in downtown Seattle", "doesn't have a car"]
```

**Reasoning**: Multi-stage retrieval ensures critical safety information is never missed, while using semantic search for preferences and recency weighting for recent context.

---

### Step 4: Conflict Resolution

```
WHEN memories conflict:

RULE 1: Recency Wins for Preferences
  IF: "loves sushi" (2 years ago) CONFLICTS WITH "trying to eat less fish" (1 month ago)
  THEN: Prioritize recent memory
  ACTION: Include both, but note the recent one is current preference
  
RULE 2: Safety Information Never Expires
  IF: "allergic to peanuts" (3 years ago) with no contradicting update
  THEN: Treat as still valid
  ACTION: Include with high priority
  
RULE 3: Explicit Updates Override
  IF: "favorite restaurant is Chez Marie" THEN "Chez Marie closed down"
  THEN: The update invalidates the original
  ACTION: Exclude the outdated fact, include the update
  
RULE 4: Frequency Indicates Strength
  IF: "mentioned loving pizza" appears 8 times vs "mentioned liking tacos" once
  THEN: Pizza preference is stronger signal
  ACTION: Weight by mention frequency

CONFLICT_RESOLUTION_OUTPUT:
  resolved_preferences: [
    {fact: "trying to reduce fish consumption", confidence: "high", source: "recent"},
    {fact: "historically loved sushi", confidence: "medium", source: "historical", note: "may be outdated"}
  ]
```

**Reasoning**: Different types of information have different "decay rates." Allergies persist; taste preferences evolve. Always preserve context about uncertainty.

---

### Step 5: Format for LLM Context

```
FORMAT retrieved memories as structured context:

=== USER MEMORY CONTEXT ===

CRITICAL (Safety):
- Dietary restriction: Vegetarian since 2023
- Allergy: Shellfish (severe)

PREFERENCES (High Confidence - Recent):
- Currently trying to eat less fish (mentioned 1 month ago)
- Prefers restaurants with outdoor seating
- Dislikes loud/crowded environments
- Budget: Usually spends $30-50 per person for nice dinners

PREFERENCES (Medium Confidence - Historical):
- Has enjoyed Italian cuisine in the past
- Mentioned wanting to try Thai food (3 months ago, not yet acted on)

RECENT CONTEXT:
- Tried Olive Garden last month, found it "just okay"
- Asked about sushi places 2 weeks ago (note: now reducing fish)

LOCATION/LOGISTICS:
- Based in downtown Seattle
- No car (prefers walkable or transit-accessible)

=== END MEMORY CONTEXT ===
```

**Reasoning**: Structured format helps the LLM parse information quickly. Confidence levels and recency notes help it weigh information appropriately. Safety information is prominently placed.

---

## Complete Algorithm Flowchart

```
┌─────────────────────────────────────────┐
│         User Query Received             │
│   "What restaurant should I try?"       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         1. ANALYZE QUERY                │
│   - Extract intent (recommendation)     │
│   - Identify domain (dining)            │
│   - Note constraints (weekend)          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    2. IDENTIFY RELEVANT CATEGORIES      │
│   - Map query to memory categories      │
│   - Prioritize safety-critical ones     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       3. MULTI-STAGE RETRIEVAL          │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ Stage 1: Safety (allergies)     │   │
│  │ → Always include, no limit      │   │
│  └──────────────────────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │ Stage 2: Semantic Search        │   │
│  │ → Top 10 by similarity          │   │
│  └──────────────────────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │ Stage 3: Recent Context         │   │
│  │ → Last 90 days, top 5           │   │
│  └──────────────────────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │ Stage 4: Location/Logistics     │   │
│  │ → 2-3 most recent               │   │
│  └──────────────────────────────────┘   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      4. RESOLVE CONFLICTS               │
│   - Recency wins for preferences        │
│   - Safety info never expires           │
│   - Note confidence levels              │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       5. FORMAT FOR LLM                 │
│   - Structured sections                 │
│   - Confidence indicators               │
│   - Clear hierarchy                     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      INJECT INTO LLM PROMPT             │
│   System: "Here's what you know..."     │
│   + User query                          │
│   → Generate personalized response      │
└─────────────────────────────────────────┘
```

---

## Key Principles

1. **Safety First**: Always retrieve and prominently display allergies/restrictions
2. **Semantic over Keyword**: Use embeddings to find conceptually related memories
3. **Recency Awareness**: Recent information often reflects current state
4. **Confidence Levels**: Let the LLM know what's certain vs. potentially outdated
5. **Context Budget**: Don't overwhelm the LLM—retrieve the most relevant subset
6. **Structured Output**: Format memories for easy parsing and prioritization
