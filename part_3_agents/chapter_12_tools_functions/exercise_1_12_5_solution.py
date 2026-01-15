# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: exercise_1_12_5_solution.py

from langchain_core.tools import Tool

# Clear, distinctive names and descriptions for search tools

tools = [
    Tool(
        name="general_web_search",
        func=lambda x: f"Web results for {x}",
        description=(
            "Search the entire web for any topic or information. "
            "Use when: Need broad information, tutorials, or general facts. "
            "Input: Any search query. "
            "Output: Mixed web results from various sources."
        )
    ),
    Tool(
        name="news_search",
        func=lambda x: f"News about {x}",
        description=(
            "Search specifically for recent news articles and current events. "
            "Use when: Need latest updates, breaking news, or recent developments. "
            "Input: News topic or event. "
            "Output: Recent news articles from last 7 days."
        )
    ),
    Tool(
        name="academic_paper_search",
        func=lambda x: f"Academic papers on {x}",
        description=(
            "Search scholarly articles, research papers, and academic journals. "
            "Use when: Need peer-reviewed research, citations, or scientific studies. "
            "Input: Academic topic or research question. "
            "Output: Academic papers with citations and abstracts."
        )
    ),
    Tool(
        name="local_business_search",
        func=lambda x: f"Local businesses: {x}",
        description=(
            "Find local businesses, stores, restaurants, and services. "
            "Use when: Need addresses, hours, reviews for physical locations. "
            "Input: 'business type in location' like 'pizza in NYC'. "
            "Output: Business listings with ratings and contact info."
        )
    ),
    Tool(
        name="social_media_search",
        func=lambda x: f"Social posts about {x}",
        description=(
            "Search social media posts, trends, and discussions. "
            "Use when: Need public opinion, trending topics, or social sentiment. "
            "Input: Topic, hashtag, or person. "
            "Output: Recent social media posts and engagement metrics."
        )
    )
]

# Print the distinctive descriptions
print("DISTINCTIVE SEARCH TOOL DESCRIPTIONS")
print("=" * 60)
for tool in tools:
    print(f"\n{tool.name}:")
    print(f"  {tool.description}")

print("\n✅ Each tool has:")
print("- Clear, specific name")
print("- When to use it")
print("- Input format")
print("- Output description")
print("- No overlap with other tools")
