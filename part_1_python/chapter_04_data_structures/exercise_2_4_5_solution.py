# From: Zero to AI Agent, Chapter 4, Section 4.5
# Exercise 2: Skill Matcher

# Job requirements and candidates
jobs = {
    "Backend Dev": {"Python", "SQL", "API", "Docker"},
    "Data Scientist": {"Python", "SQL", "ML", "Statistics"},
    "Frontend Dev": {"JavaScript", "HTML", "CSS", "React"}
}

candidates = {
    "John": {"Python", "SQL", "API", "Docker", "ML"},
    "Jane": {"JavaScript", "HTML", "CSS", "Vue"},
    "Bob": {"Python", "SQL", "Statistics"}
}

# Find perfect matches
print("Perfect Matches:")
for job_title, required in jobs.items():
    for name, skills in candidates.items():
        if required.issubset(skills):
            print(f"  {name} -> {job_title}")

# Partial matches with percentage
print("\nPartial Matches:")
for job_title, required in jobs.items():
    print(f"\n{job_title}:")
    for name, skills in candidates.items():
        matching = required & skills
        percentage = (len(matching) / len(required)) * 100
        if 0 < percentage < 100:
            print(f"  {name}: {percentage:.0f}% match")

# Missing skills
print("\nMissing Skills:")
for name, skills in candidates.items():
    for job_title, required in jobs.items():
        missing = required - skills
        if missing and len(missing) < len(required):
            print(f"  {name} for {job_title}: needs {missing}")

# Training recommendations
print("\nTraining Recommendations:")
all_required = set.union(*jobs.values())
for name, skills in candidates.items():
    should_learn = all_required - skills
    if should_learn:
        print(f"  {name}: Consider learning {list(should_learn)[:2]}")
