# Exercise 2 Solution: Design a Memory Schema

## Personal Finance Assistant - Memory Schema

---

## 1. Short-Term Memory (During Budgeting Conversation)

```
short_term_memory:
  conversation_history:
    - messages[]              # Recent user/assistant exchanges
    - current_topic           # "monthly budget", "savings goal", "expense tracking"
    - conversation_start_time
  
  working_state:
    - current_calculations:
        - income_total
        - expense_total
        - remaining_budget
        - category_breakdowns[]
    - pending_actions[]       # Things user asked to do but hasn't confirmed
    - draft_budget            # Budget being actively edited
  
  session_context:
    - referenced_accounts[]   # Accounts mentioned this session
    - time_period_discussed   # "March 2024", "Q1", "this year"
    - comparison_baseline     # If comparing to previous periods
```

**Purpose**: Enable coherent multi-turn conversation about budgets without losing track of what's being discussed.

---

## 2. Long-Term Memory (Across Sessions)

```
long_term_memory:
  user_profile:
    - name
    - preferred_currency
    - communication_preferences:
        - detail_level          # "brief" | "detailed"
        - visualization_preference  # "charts" | "tables" | "text"
    - timezone
    - created_at
    - last_active

  financial_profile:
    - income_sources[]:
        - source_name
        - amount
        - frequency            # "monthly", "bi-weekly", "annual"
        - last_updated
    - recurring_expenses[]:
        - category
        - description
        - amount
        - frequency
        - last_updated
    - accounts[]:
        - account_nickname     # "main checking", "emergency fund"
        - account_type         # "checking", "savings", "investment"
        - institution          # (optional)
    - financial_goals[]:
        - goal_name            # "vacation fund", "emergency savings"
        - target_amount
        - current_amount
        - target_date
        - priority

  preferences_and_patterns:
    - spending_categories_of_concern[]  # Categories user often asks about
    - budget_style             # "strict", "flexible", "50-30-20"
    - savings_priority         # "aggressive", "moderate", "minimal"
    - notification_preferences:
        - budget_alerts        # true/false
        - goal_milestones      # true/false

  historical_context:
    - past_budgets[]:
        - period
        - planned_vs_actual
        - summary
    - significant_financial_events[]:
        - event               # "job change", "major purchase", "debt payoff"
        - date
        - impact_notes
    - conversation_summaries[]:
        - date
        - topics_discussed
        - decisions_made
        - action_items
```

**Purpose**: Personalize advice, remember user's financial situation, and provide continuity across sessions.

---

## 3. Short-Term → Long-Term Transfer Rules

### Automatic Transfers (High Confidence)

| Trigger | What Gets Stored | Long-Term Location |
|---------|------------------|-------------------|
| User states income | Amount, frequency, source | `financial_profile.income_sources` |
| User mentions recurring bill | Description, amount, frequency | `financial_profile.recurring_expenses` |
| User sets a goal | Goal details | `financial_profile.financial_goals` |
| User expresses preference | The preference | `preferences_and_patterns` |
| User mentions account | Account nickname, type | `financial_profile.accounts` |

### Prompted Transfers (Ask User)

| Trigger | Prompt |
|---------|--------|
| Session ends with budget created | "Would you like me to remember this budget for future reference?" |
| Major financial change discussed | "Should I update your profile to reflect this change?" |
| Detailed conversation about spending | "Want me to save a summary of what we discussed?" |

### End-of-Session Summary

At conversation end, automatically generate and store:
```
conversation_summary:
  - date: "2024-03-15"
  - duration_minutes: 23
  - main_topics: ["monthly budget review", "vacation savings"]
  - key_decisions: ["increase dining budget by $50", "start vacation fund"]
  - action_items: ["review subscriptions next week"]
  - sentiment: "productive"  # optional
```

---

## 4. What Should NOT Be Stored

### Never Store

| Information Type | Reason |
|-----------------|--------|
| Bank account numbers | Security risk - use tokenized references only |
| Passwords/PINs | Critical security vulnerability |
| Social Security numbers | PII with no legitimate use case |
| Full credit card numbers | PCI compliance violation |
| Investment trade details | Liability and regulatory concerns |
| Exact transaction data | Privacy; use aggregates instead |

### Store with Caution (or Not at All)

| Information Type | Concern | Recommendation |
|-----------------|---------|----------------|
| Exact salary amount | Sensitive PII | Store ranges or user-chosen labels |
| Debt amounts | Potentially embarrassing | Store only if user explicitly shares |
| Spending on sensitive categories | Privacy | Aggregate or omit (gambling, adult content, etc.) |
| Net worth | High-sensitivity | Only if user requests tracking |

### Ephemeral Information (Short-Term Only)

| Information Type | Reason |
|-----------------|--------|
| Today's stock prices | Outdated within hours |
| Current exchange rates | Changes constantly |
| "I'm feeling stressed about money today" | Momentary state, not persistent trait |
| Intermediate budget calculations | No value after session |

---

## Schema Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     LONG-TERM MEMORY                        │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ User        │  │ Financial   │  │ Historical       │    │
│  │ Profile     │  │ Profile     │  │ Context          │    │
│  │             │  │             │  │                  │    │
│  │ • name      │  │ • income    │  │ • past budgets   │    │
│  │ • prefs     │  │ • expenses  │  │ • events         │    │
│  │ • timezone  │  │ • accounts  │  │ • summaries      │    │
│  │             │  │ • goals     │  │                  │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
         ▲                                    │
         │ Transfer (evaluated)               │ Retrieve (on relevance)
         │                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                     SHORT-TERM MEMORY                       │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ Conversation    │  │ Working State                   │  │
│  │ History         │  │                                 │  │
│  │                 │  │ • current calculations          │  │
│  │ • messages      │  │ • draft budget                  │  │
│  │ • current topic │  │ • pending actions               │  │
│  │ • start time    │  │ • referenced accounts           │  │
│  └─────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Design Principles

1. **Privacy by Default**: Store the minimum needed; prefer aggregates over specifics
2. **User Control**: Let users see, edit, and delete their stored information
3. **Staleness Awareness**: Track `last_updated` for financial data that changes
4. **Explicit over Implicit**: Ask before storing sensitive financial details
5. **Separation of Concerns**: Keep identity data separate from financial data for security
