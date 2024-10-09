from .app import db
from .app import login_manager
from flask_login import UserMixin


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Author {self.id} {self.name}>"


class Categorie(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return f"<Categorie {self.name}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100))
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(200))

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship(
        "Author", backref=db.backref("books", lazy="dynamic"))

    # need many to many
    # https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
    # categories_name = db.Column(
    #     db.String(50), db.ForeignKey("Categorie.name"))
    # categories = db.relationship(
    #     "Categorie", backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        return f"<Book {self.id} {self.title} {self.price} {self.author} {self.Categorie}>"

class Favorite(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    # books_name = db.Column(
    #     db.String(50), db.ForeignKey("Book.id"))
    # books = db.relationship(
    #     "Book", backref=db.backref("favorites", lazy="dynamic"))

    def __repr__(self):
        return f"<Favorite {self.name}>"

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    favorite_name = db.Column(
        db.String(50), db.ForeignKey("Favorite.name"))
    # favorite = db.relationship(
    #     "Favorite", backref=db.backref("users", lazy="dynamic"))

    def get_id(self):
        return f"<User {self.username}>"


def get_sample():
    return Book.query.limit(50).all()


def get_book(id: int):
    return Book.query.get(id)


def get_author(id: int):
    return Author.query.get(id)


def get_book_by_author(id: int):
    return Author.query.get_or_404(id).books.all()


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
