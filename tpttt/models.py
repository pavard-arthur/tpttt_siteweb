from .app import db
from .app import login_manager
from flask_login import UserMixin


class Author(db.Model):
    Auth_id = db.Column(db.Integer, primary_key=True)
    Auth_name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Author {self.Auth_id} {self.Auth_name}>"


class Categorie(db.Model):
    Cat_name = db.Column(db.String(50), primary_key=True)

    Cat_Book = db.relationship("Book",secondary="BookCat",backref=db.backref("Books_Cat", lazy="dynamic"))


    def __repr__(self):
        return f"<Categorie {self.Cat_name}>"


class Book(db.Model):
    Book_id = db.Column(db.Integer, primary_key=True)
    Book_img = db.Column(db.String(100))
    Book_price = db.Column(db.Float)
    Book_title = db.Column(db.String(100))
    Book_url = db.Column(db.String(200))

    Book_author_id = db.Column(db.Integer, db.ForeignKey("author.Auth_id"))
    Book_author = db.relationship("Author", backref=db.backref("Auth_books", lazy="dynamic"))

    Book_Cat = db.relationship("Categorie",secondary="BookCat",backref=db.backref("Cat_Books", lazy="dynamic"))


    def __repr__(self):
        return f"<Book {self.Book_id} {self.Book_title} {self.Book_price} {self.Book_author} {self.Book_categories}>"

class Favorite(db.Model):
    FAV_id = db.Column(db.Integer, primary_key=True)

    FAV_books_id = db.Column(db.Integer, db.ForeignKey("Book.Book_id"))
    FAV_books = db.relationship("Book", backref=db.backref("Book_FAV", lazy="dynamic"))

    def __repr__(self):
        return f"<Favorite {self.name}>"

class BookCat(db.Model):
    # need many to many
    # https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
    Book_Cat_id = db.Column(db.Integer, primary_key=True)
    Book_Cat_Book_id = db.Column(db.Integer, db.ForeignKey("Book.Book_id"))
    Book_Cat_Cat_name = db.Column(db.String(50), db.ForeignKey("Categorie.Cat_name"))

class User(db.Model, UserMixin):
    U_username = db.Column(db.String(50), primary_key=True)
    U_password = db.Column(db.String(64))

    U_FAV_if = db.Column(db.String(50), db.ForeignKey("Favorite.FAV_id"))
    U_FAV = db.relationship("Favorite", backref=db.backref("FAV_U", lazy="dynamic"))

    def get_id(self):
        return f"<User {self.U_username}>"


def get_sample():
    return Book.query.limit(50).all()


def get_book(id: int):
    return Book.query.get(id)


def get_author(id: int):
    return Author.query.get(id)


def get_book_by_author(id: int):
    return Author.query.get_or_404(id).Auth_books.all()


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
