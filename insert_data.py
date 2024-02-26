import json
from sqlalchemy.orm import Session
from db_schema import Author, Genre, Book, Publisher, Borrower, Transaction, Language, BookCopy, BookStatus, BookReview
from datetime import datetime

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def insert_data(session: Session, data: list):
    for entry in data:
        authors = [Author(**author) for author in entry.get('authors', [])]
        genres = [Genre(**genre) for genre in entry.get('genres', [])]

        session.add_all(authors + genres)
        session.flush()  # Flush the session to get the inserted IDs

        for book_data in entry.get('books', []):
            authors_data = book_data.get('authors', [])
            if authors_data:
                author_id = next((author.id for author in authors if author.name == authors_data[0]['name']), None)
                book_data['author_id'] = author_id
            else:
                print("Warning: 'authors' key not found in book_data.")

            genre_ids = [next((genre.id for genre in genres if genre.name == genre_name), None) for genre_name in book_data.get('genres', [])]

            # Filter out None values from genre_ids
            genre_ids = [genre_id for genre_id in genre_ids if genre_id is not None]

            book_data['genres'] = genre_ids

            if 'publication_date' in book_data and isinstance(book_data['publication_date'], str):
                book_data['publication_date'] = datetime.strptime(book_data['publication_date'], '%Y-%m-%d').date()

            book_instance = Book(**book_data)
            session.add(book_instance)

        publishers = [Publisher(**publisher) for publisher in entry.get('publishers', [])]
        borrowers = [Borrower(**borrower) for borrower in entry.get('borrowers', [])]

        transactions_data = entry.get('transactions', [])
        if isinstance(transactions_data, dict):
            transactions_data = [transactions_data] 

        for transaction_data in transactions_data:
            if 'check_out_date' in transaction_data and isinstance(transaction_data['check_out_date'], str):
                transaction_data['check_out_date'] = datetime.strptime(transaction_data['check_out_date'], '%Y-%m-%d').date()

            if 'return_date' in transaction_data and isinstance(transaction_data['return_date'], str):
                transaction_data['return_date'] = datetime.strptime(transaction_data['return_date'], '%Y-%m-%d').date()

        transactions = [Transaction(**transaction_data) for transaction_data in transactions_data]

        languages = [Language(**language) for language in entry.get('languages', [])]
        book_copies = [BookCopy(**copy) for copy in entry.get('book_copies', [])]
        book_statuses = [BookStatus(**status) for status in entry.get('book_statuses', [])]
        book_reviews = [BookReview(**review) for review in entry.get('book_reviews', [])]

        # Add all objects to the session
        session.add_all(authors + genres + publishers + borrowers +
                        transactions + languages + book_copies + book_statuses + book_reviews)

    # Commit the changes
    session.commit()

