from book import Book

class Library:
    def __init__(self, books):
        self.books = books

    def add_book(self, book: Book) -> bool:
        if not isinstance(book, Book):
            raise TypeError("book must be an instance of Book")
        # Kontrola duplicity podľa (title, author, year)
        for existing in self.books:
            if (existing.title == book.title and
                existing.author == book.author and
                existing.year == book.year):
                return False
        self.books.append(book)
        return True

    def list_books(self) -> list[str]:
        return [str(book) for book in self.books]

    def find_book(self):
        pass

    def borrow_book(self):
        pass

    def return_book(self):
        pass