class Book:
    def __init__(self, title, author, year, is_available):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = is_available

    def __str__(self):
        return f"title: {self.title} ({self.year}), author: {self.author} -> {'is available' if self.is_available else 'is not available'}"