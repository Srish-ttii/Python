import json
from pathlib import Path
import logging


logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"

    def to_dict(self):
        """Convert object to dict for JSON saving"""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }



class LibraryInventory:
    def __init__(self, file_path="books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()


    def load_books(self):
        try:
            if not self.file_path.exists():
                self.save_books()  # create empty file
                return

            data = json.loads(self.file_path.read_text())
            self.books = [Book(**item) for item in data]

        except Exception as e:
            logging.error("Error loading book data", exc_info=True)
            self.books = []


    def save_books(self):
        try:
            data = [book.to_dict() for book in self.books]
            self.file_path.write_text(json.dumps(data, indent=4))
        except Exception as e:
            logging.error("Error saving book data", exc_info=True)


    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        logging.info(f"Book added: {book.title}")


    def search_by_title(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]


    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    # Display all
    def display_all(self):
        return self.books




def menu():
    library = LibraryInventory()

    while True:
        print("\n==== LIBRARY INVENTORY MANAGER ====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Search Book")
        print("5. View All Books")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")

            book = Book(title, author, isbn)
            library.add_book(book)
            print("Book added successfully!")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = library.search_by_isbn(isbn)

            if book and book.issue():
                library.save_books()
                print("Book issued successfully!")
            else:
                print("Cannot issue book (maybe already issued).")

        
        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = library.search_by_isbn(isbn)

            if book and book.return_book():
                library.save_books()
                print("Book returned successfully!")
            else:
                print("Cannot return book.")

        
        elif choice == "4":
            keyword = input("Enter title keyword: ")
            results = library.search_by_title(keyword)

            if results:
                print("\nSearch Results:")
                for r in results:
                    print(r)
            else:
                print("No books found.")

        
        elif choice == "5":
            books = library.display_all()

            if not books:
                print("No books available.")
            else:
                print("\n--- All Books ---")
                for book in books:
                    print(book)

        # 6. EXIT
        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print("Invalid choice! Please try again.")



if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        logging.error("Unexpected Error", exc_info=True)
        print("An error occurred. Check logs.")
