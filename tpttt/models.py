from .app import db
from .app import login_manager
from flask_login import UserMixin

# Many-to-many relationship for favorite books
favorite_books = db.Table(
    'favorite_books',
    db.Column('user_id', db.String(50), db.ForeignKey('user.U_username')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.B_id')))


class Author(db.Model):
    A_id = db.Column(db.Integer, primary_key=True)
    A_name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Author {self.A_id} {self.A_name}>"


class Genre(db.Model):
    C_id = db.Column(db.Integer, primary_key=True)
    C_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Genre {self.C_id} {self.C_name}>"

class Book(db.Model):
    B_id = db.Column(db.Integer, primary_key=True)
    B_img = db.Column(db.String(100))
    B_price = db.Column(db.Float)
    B_title = db.Column(db.String(100))
    B_url = db.Column(db.String(200))

    # Foreign key and relationship with Author
    A_id = db.Column(db.Integer, db.ForeignKey("author.A_id"))
    author = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))

    # Foreign key and relationship with Genre
    C_id = db.Column(db.Integer, db.ForeignKey("genre.C_id"))
    genre = db.relationship("Genre", backref=db.backref("books", lazy=True))

    def __repr__(self):
        return f"<Book {self.B_id} {self.B_title}>"



class User(db.Model, UserMixin):
    U_username = db.Column(db.String(50), primary_key=True)
    U_password = db.Column(db.String(64))

    # Relationship for favorite books
    favorites = db.relationship('Book',
                                secondary=favorite_books,
                                lazy='subquery',
                                backref=db.backref('favorited_by', lazy=True))

    def get_id(self):
        return self.U_username


# GET
def get_sample():
    return Book.query.limit(18).all()


def get_book(id: int):
    return Book.query.get(id)


def get_author(id: int):
    return Author.query.get(id)


def get_book_by_author(id: int):
    return Author.query.get_or_404(id).books.all()


def get_genre(id: int):
    return Genre.query.get(id)


def get_books_by_genre(id: int):
    return Genre.query.get_or_404(id).books.all()


def get_favorites(user_id: str):
    return User.query.get(user_id).favorites.all()


# ADD
def add_book(title, price, url, img, author_id, genres):
    book = Book(
        B_title=title,
        B_price=price,
        B_url=url,
        B_img=img,
        author_id=author_id,
        genres=genres  # Handle many-to-many relationship
    )
    db.session.add(book)
    db.session.commit()


def add_author(name):
    author = Author(A_name=name)
    db.session.add(author)
    db.session.commit()


def add_genre(name):
    genre = Genre(C_name=name)
    db.session.add(genre)
    db.session.commit()


# EDIT
def update_book(book, title, price, url, img, genres):
    book.B_title = title
    book.B_price = price
    book.B_url = url
    book.B_img = img
    book.genres = genres  # Update the many-to-many relationship
    db.session.commit()


def update_author(author, name):
    author.A_name = name
    db.session.commit()


def update_genre(genre, name):
    genre.C_name = name
    db.session.commit()


# FAVORITE


def add_favorite(user_id: str, book_id: int):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if book not in user.favorites:
        user.favorites.append(book)
        db.session.commit()


def remove_favorite(user_id: str, book_id: int):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if book in user.favorites:
        user.favorites.remove(book)
        db.session.commit()


# SEARCH
def search_books(query: str):
    return Book.query.filter(
        db.or_(Book.B_title.ilike(f"%{query}%"),
               Book.B_price.ilike(f"%{query}%"))).all()


def search_authors(query: str):
    return Author.query.filter(Author.A_name.ilike(f"%{query}%")).all()


def search_genres(query: str):
    return Genre.query.filter(Genre.C_name.ilike(f"%{query}%")).all()


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
