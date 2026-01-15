# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: import_best_practices.py

# Good practices for organizing imports

# 1. Standard library imports first
import os
import sys
from datetime import datetime

# 2. Related third-party imports next
import numpy as np
import pandas as pd
import requests

# 3. Local application imports last
# from my_module import my_function

# 4. Organize imports alphabetically within each group
# 5. One import per line (easier to read)
# 6. Avoid wildcard imports (from module import *)
# 7. Use meaningful aliases