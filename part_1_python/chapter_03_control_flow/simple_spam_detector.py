# From: Zero to AI Agent, Chapter 3, Section 3.1
# simple_spam_detector.py
# A glimpse into how AI makes decisions!

email_subject = input("Enter email subject: ").lower()
sender = input("Enter sender email: ").lower()

spam_score = 0

# Check for spam indicators
if "free" in email_subject:
    spam_score += 2
if "winner" in email_subject:
    spam_score += 3
if "click here" in email_subject:
    spam_score += 3
if "@suspiciousdomain.com" in sender:
    spam_score += 5

# Make a decision based on the score
print(f"\nSpam Score: {spam_score}")
if spam_score >= 5:
    print("⚠️ HIGH RISK: This is likely spam!")
elif spam_score >= 3:
    print("⚡ MEDIUM RISK: This might be spam.")
else:
    print("✅ LOW RISK: This appears legitimate.")
