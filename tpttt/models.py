from .app import db
from .app import login_manager
from flask_login import UserMixin


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Author {self.id} {self.name}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100))
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(200))

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author",
                             backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        return f"<Book {self.id} {self.title}>"

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    def get_id(self):
        return self.username

def get_sample():
    return Book.query.limit(50).all()

def get_book(id : int):
    return Book.query.get(id)

def get_author(id : int):
    return Author.query.get(id)

def get_book_by_author(id : int):
    return Author.query.get_or_404(id).books.all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
