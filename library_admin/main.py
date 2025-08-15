import json
import os
import random
from book import Book
from library import Library

FILE_PATH = "books.json"

def book_to_dict(book: Book) -> dict:
    return {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "is_available": book.is_available,
    }

def dict_to_book(d: dict) -> Book:
    return Book(
        d.get("title", ""),
        d.get("author", ""),
        int(d.get("year", 0)),
        bool(d.get("is_available", True)),
    )

def load_books_from_json(path: str) -> list[Book]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [dict_to_book(item) for item in data]
    except Exception as e:
        print(f"Chyba pri načítaní súboru: {e}")
        return []

def save_books_to_json(path: str, books: list[Book]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([book_to_dict(b) for b in books], f, ensure_ascii=False, indent=2)
        print(f"Zoznam kníh bol uložený do {path}")
    except Exception as e:
        print(f"Chyba pri ukladaní súboru: {e}")

def seed_sample_books() -> list[Book]:
    books_data = [
        ("1984", "George Orwell", 1949),
        ("To Kill a Mockingbird", "Harper Lee", 1960),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
        ("Pride and Prejudice", "Jane Austen", 1813),
        ("Moby-Dick", "Herman Melville", 1851),
        ("The Catcher in the Rye", "J.D. Salinger", 1951),
        ("Brave New World", "Aldous Huxley", 1932),
        ("War and Peace", "Leo Tolstoy", 1869),
        ("The Hobbit", "J.R.R. Tolkien", 1937),
        ("The Lord of the Rings", "J.R.R. Tolkien", 1954),
        ("Crime and Punishment", "Fyodor Dostoevsky", 1866),
    ]
    return [Book(t, a, y, random.choice([True, False])) for t, a, y in books_data]

def print_menu():
    print("\n=== MENU ===")
    print("1. Pridať novú knihu")
    print("2. Vypísať všetky knihy")
    print("3. Vyhľadať knihu podľa názvu alebo autora")
    print("4. Označiť knihu ako požičanú alebo vrátenú")
    print("5. Uložiť zoznam kníh do JSON súboru")
    print("Q. Koniec")

def prompt_new_book() -> Book | None:
    title = input("Názov: ").strip()
    author = input("Autor: ").strip()
    year_str = input("Rok vydania: ").strip()
    if not title or not author or not year_str:
        print("Názov, autor a rok musia byť vyplnené.")
        return None
    try:
        year = int(year_str)
    except ValueError:
        print("Rok musí byť číslo.")
        return None
    avail_str = input("Je dostupná? (y/n): ").strip().lower()
    is_available = avail_str in ("y", "yes", "áno", "ano", "a")
    return Book(title, author, year, is_available)

def search_books(library: Library, query: str) -> list[Book]:
    q = query.lower().strip()
    return [b for b in library.books if q in b.title.lower() or q in b.author.lower()]

def choose_from_list(items: list[str], header: str = "Výsledky:") -> int | None:
    if not items:
        print("Žiadne položky na výber.")
        return None
    print(header)
    for i, txt in enumerate(items, start=1):
        print(f"{i}. {txt}")
    sel = input("Zvoľ číslo (Enter pre zrušenie): ").strip()
    if not sel:
        return None
    try:
        idx = int(sel)
        if 1 <= idx <= len(items):
            return idx - 1
        print("Neplatná voľba.")
        return None
    except ValueError:
        print("Prosím zadaj číslo.")
        return None

def main():
    # Načítaj knihy zo súboru, inak seedni ukážkové
    loaded = load_books_from_json(FILE_PATH)
    if loaded:
        print(f"Načítaných {len(loaded)} kníh zo súboru {FILE_PATH}.")
        library = Library(loaded)
    else:
        print("Súbor s knihami nenájdený, vytváram ukážkové knihy.")
        library = Library(seed_sample_books())

    while True:
        print_menu()
        choice = input("Vyber možnosť: ").strip().lower()

        if choice == "1":
            new_book = prompt_new_book()
            if new_book:
                if library.add_book(new_book):
                    print("Kniha pridaná.")
                else:
                    print("Kniha už existuje (duplicitný názov/autor/rok).")

        elif choice == "2":
            lines = library.list_books()
            if not lines:
                print("Žiadne knihy v knižnici.")
            else:
                print("\n".join(lines))

        elif choice == "3":
            q = input("Zadaj názov alebo autora: ").strip()
            results = search_books(library, q)
            if not results:
                print("Nenašli sa žiadne knihy.")
            else:
                for b in results:
                    print(str(b))

        elif choice == "4":
            q = input("Zadaj názov alebo autora (pre výber knihy): ").strip()
            results = search_books(library, q)
            if not results:
                print("Nenašli sa žiadne knihy.")
                continue
            idx = choose_from_list([str(b) for b in results], "Nájdené knihy:")
            if idx is None:
                continue
            book = results[idx]
            action = input("Zadaj 'p' pre požičať alebo 'v' pre vrátiť: ").strip().lower()
            if action == "p":
                if not book.is_available:
                    print("Kniha je už požičaná.")
                else:
                    book.is_available = False
                    print("Kniha označená ako požičaná.")
            elif action == "v":
                if book.is_available:
                    print("Kniha je už dostupná.")
                else:
                    book.is_available = True
                    print("Kniha označená ako vrátená.")
            else:
                print("Neznáma akcia.")

        elif choice == "5":
            save_books_to_json(FILE_PATH, library.books)

        elif choice == "q":
            # Pri odchode sa môže automaticky uložiť (voliteľné)
            should_save = input("Uložiť zmeny pred ukončením? (y/n): ").strip().lower()
            if should_save in ("y", "yes", "áno", "ano", "a"):
                save_books_to_json(FILE_PATH, library.books)
            print("Dovidenia!")
            break

        else:
            print("Neplatná voľba. Skús znova.")

if __name__ == "__main__":
    main()

