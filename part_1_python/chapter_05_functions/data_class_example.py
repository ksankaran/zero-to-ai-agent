# From: Zero to AI Agent, Chapter 5, Section 5.8
# data_class_example.py - Using classes for data organization

class Contact:
    """Store contact information"""

    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def display(self):
        info = f"Name: {self.name}\nEmail: {self.email}"
        if self.phone:
            info += f"\nPhone: {self.phone}"
        return info

    def send_email(self, message):
        # In real code, this would actually send an email
        return f"Sending to {self.email}: {message}"


# Create contacts
friend = Contact("Alex", "alex@email.com", "555-1234")
colleague = Contact("Jordan", "jordan@work.com")

print(friend.display())
print()
print(colleague.send_email("Meeting at 3pm"))
