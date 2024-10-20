import datetime
from .app import app, db , login_manager
import tpttt.models as models
from .models import User, Author, Genre
from flask import render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, URL, NumberRange
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Forms


class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        
        return user if passwd == user.U_password else None



class GenreForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Genre Name", validators=[DataRequired()])
    submit = SubmitField("Save")


class BookForm(FlaskForm):
    id = HiddenField("id")  # Optional, for editing an existing book
    title = StringField("Title", validators=[DataRequired()])
    price = FloatField("Price",
                       validators=[DataRequired(),
                                   NumberRange(min=0)])
    url = StringField("URL", validators=[DataRequired(), URL()])
    img = StringField("Image URL", validators=[DataRequired(), URL()])

    # SelectField for author, assuming you'll query all authors from the database
    author_id = QuerySelectField(
        "Author",
        query_factory=lambda: Author.query.all(
        ),  # Fetch authors for the dropdown
        get_label="A_name",  # Assuming `A_name` is the author name attribute
        allow_blank=False)

    # SelectMultipleField for genres (many-to-many relationship)
    genres = QuerySelectMultipleField(
        "Genres",
        query_factory=lambda: Genre.query.all(),  # Fetch all genres
        get_label="C_name",  # Assuming `C_name` is the genre name attribute
        allow_blank=True)

    submit = SubmitField("Save")


# main page
@app.route("/")
def home():
    books = models.get_sample()
    return render_template("home.html", title="My Books!", books=books)


# GET
@app.route("/book/<int:id>")
def book(id):
    book = models.get_book(id)
    # print(book)
    return render_template("book.html", book=book)


@app.route("/author/<int:id>")
def author(id):
    author = models.get_author(id)
    books = models.get_book_by_author(id)
    return render_template("author.html", author=author, books=books)


@app.route("/genre/<int:id>")
def genre(id):
    genre = models.get_genre(id)
    books = models.get_books_by_genre(id)
    return render_template("genre.html", genre=genre, books=books)


# LOGIN
@app.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.get_authenticated_user()
        if user:
            login_user(user, remember=True)  
            next_url = form.next.data or url_for("home")
            return redirect(next_url)
    return render_template("login.html", form=form)



@app.route("/logout/")
def logout():
    print("WARNING : LOGOUT")
    logout_user()
    return redirect(url_for('home'))


# SEARCH
@app.route("/search")
def search():
    query = request.args.get('query', '')
    books = models.search_books(query) if query else []
    authors = models.search_authors(query) if query else []
    genres = models.search_genres(query) if query else []
    return render_template("search.html",
                           books=books,
                           authors=authors,
                           genres=genres)


# ADD Routes
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/add/book", methods=("GET", "POST"))
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        models.add_book(
            title=form.title.data,
            price=form.price.data,
            url=form.url.data,
            img=form.img.data,
            author_id=form.author_id.data,
            genres=form.genres.data  # Handle many-to-many relationship
        )
        return redirect(url_for("home"))
    return render_template("add_book.html", form=form)


@app.route("/add/author", methods=("GET", "POST"))
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        models.add_author(name=form.name.data)
        return redirect(url_for("home"))
    return render_template("add_author.html", form=form)


@app.route("/add/genre", methods=("GET", "POST"))
@login_required
def add_genre():
    form = GenreForm()
    if form.validate_on_submit():
        models.add_genre(name=form.name.data)
        return redirect(url_for("home"))
    return render_template("add_genre.html", form=form)


# EDIT Routes
@app.route("/edit")
def edit():
    # raw dog fetch all from model
    authors = models.Author.query.all()  
    books = models.Book.query.all()      
    genres = models.Genre.query.all()    
    return render_template("edit.html", authors=authors, books=books, genres=genres)


@app.route("/edit/book/<int:id>", methods=("GET", "POST"))
@login_required
def edit_book(id):
    book = models.get_book(id)
    form = BookForm(obj=book) 
    if form.validate_on_submit():
        models.update_book(
            book,
            title=form.title.data,
            price=form.price.data,
            url=form.url.data,
            img=form.img.data,
            genres=form.genres.data  # Update the many-to-many relationship
        )
        return redirect(url_for("book", id=id))
    return render_template("edit_book.html",book=book, form=form)


@app.route("/edit/author/<int:id>", methods=("GET", "POST"))
@login_required
def edit_author(id):
    author = models.get_author(id)
    form = AuthorForm(obj=author) 
    if form.validate_on_submit():
        models.update_author(author, name=form.name.data)
        return redirect(url_for("author", id=id))
    return render_template("edit_author.html", author=author,form=form)


@app.route("/edit/genre/<int:id>", methods=("GET", "POST"))
@login_required
def edit_genre(id):
    genre = models.get_genre(id)
    form = GenreForm(obj=genre) 
    if form.validate_on_submit():
        models.update_genre(genre, name=form.name.data)
        return redirect(url_for("genre", id=id))
    return render_template("edit_genre.html",genre=genre, form=form)


# REMOVE
# #rawdog
@app.route("/remove/book/<int:id>", methods=("GET", "POST"))
@login_required
def remove_book(id):
    book = models.get_book(id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/remove/author/<int:id>", methods=("GET", "POST"))
@login_required
def remove_author(id):
    author = models.get_author(id)
    if author:
        db.session.delete(author)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/remove/genre/<int:id>", methods=("GET", "POST"))
@login_required
def remove_genre(id):
    genre = models.get_genre(id)
    if genre:
        db.session.delete(genre)
        db.session.commit()
    return redirect(url_for("home"))


# FAVORITE
@app.route("/favorites/")
@login_required
def favorites():
    favorites = models.get_favorites(current_user.U_username)
    return render_template("favorites.html", books=favorites)


@app.route("/add/favorite/<int:book_id>", methods=("GET", "POST"))
@login_required
def add_to_favorites(book_id):
    models.add_favorite(current_user.U_username, book_id)
    return redirect(url_for("favorites"))


@app.route("/remove/favorite/<int:book_id>", methods=("GET", "POST"))
@login_required
def remove_from_favorites(book_id):
    models.remove_favorite(current_user.U_username, book_id)
    return redirect(url_for("favorites"))
