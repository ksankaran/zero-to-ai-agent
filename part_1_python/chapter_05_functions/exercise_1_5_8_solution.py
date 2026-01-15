# From: Zero to AI Agent, Chapter 5, Section 5.8
# Exercise 1: Book Class

class Book:
    """A class representing a book with reading progress tracking"""

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.current_page = 0

    def read(self, num_pages):
        """Advance the current page by num_pages"""
        self.current_page += num_pages
        if self.current_page > self.pages:
            self.current_page = self.pages
        print(f"Read {num_pages} pages. Now on page {self.current_page}.")

    def get_progress(self):
        """Return the reading progress as a percentage"""
        if self.pages == 0:
            return 0
        percentage = (self.current_page / self.pages) * 100
        return round(percentage, 1)

    def is_finished(self):
        """Check if the book has been completely read"""
        return self.current_page >= self.pages

    def display_info(self):
        """Display book information and progress"""
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.current_page}/{self.pages}")
        print(f"Progress: {self.get_progress()}%")
        if self.is_finished():
            print("Status: Finished!")
        else:
            print(f"Status: {self.pages - self.current_page} pages remaining")


# Test the Book class
print("=" * 40)
print("BOOK READING TRACKER")
print("=" * 40)

# Create a book
my_book = Book("Python Crash Course", "Eric Matthes", 544)
my_book.display_info()

print()

# Read some pages
my_book.read(100)
my_book.read(150)
print(f"Progress: {my_book.get_progress()}%")
print(f"Finished? {my_book.is_finished()}")

print()

# Finish the book
my_book.read(300)
my_book.display_info()
