from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///library_db.db', echo=True)
Base = declarative_base()

book_genre_association = Table('book_genre_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship('Book', back_populates='author')

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship('Book', secondary=book_genre_association, back_populates='genres')

class Borrower(Base):
    __tablename__ = 'borrowers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    transactions = relationship('Transaction', back_populates='borrower')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    borrower_id = Column(Integer, ForeignKey('borrowers.id'))
    check_out_date = Column(Date)
    return_date = Column(Date)

    book = relationship('Book')
    borrower = relationship('Borrower')

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship('Book', back_populates='language')

class BookCopy(Base):
    __tablename__ = 'book_copies'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    status_id = Column(Integer, ForeignKey('book_statuses.id'))

    book = relationship('Book', back_populates='copies')
    status = relationship('BookStatus', back_populates='copies')

class BookStatus(Base):
    __tablename__ = 'book_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    copies = relationship('BookCopy', back_populates='status')

class BookReview(Base):
    __tablename__ = 'book_reviews'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    reviewer_name = Column(String)
    rating = Column(Integer)
    comment = Column(String)

    book = relationship('Book', back_populates='reviews')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))
    language_id = Column(Integer, ForeignKey('languages.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    author = relationship('Author', back_populates='books')
    genres = relationship('Genre', secondary=book_genre_association, back_populates='books')
    language = relationship('Language', back_populates='books')
    copies = relationship('BookCopy', back_populates='book')
    publisher = relationship('Publisher', back_populates='books')
    reviews = relationship('BookReview', back_populates='book')


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='publisher')

# Create tables in the database
Base.metadata.create_all(engine)
