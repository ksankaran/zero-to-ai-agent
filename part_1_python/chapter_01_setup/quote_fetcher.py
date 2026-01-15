# quote_fetcher.py
# From: Zero to AI Agent, Chapter 1, Section 1.4

import requests
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored text
init()

print("=" * 50)
print(f"{Fore.CYAN}QUOTE OF THE MOMENT{Style.RESET_ALL}")
print("=" * 50)

# Fetch a random quote from an API
response = requests.get("https://dummyjson.com/quotes/random")
print("")
print(f"{Fore.YELLOW}Response from API:{Style.RESET_ALL}")
print(response.text)
print("")
print(f"{Fore.GREEN}If you see JSON above, both packages work!{Style.RESET_ALL}")
print("- requests: fetched data from the internet")
print("- colorama: added colors to this text")
print("=" * 50)
