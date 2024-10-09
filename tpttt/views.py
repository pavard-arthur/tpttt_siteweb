from .app import app , db
import tpttt.models as models
from .models import User
from flask import render_template , redirect , url_for ,request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField , PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user , current_user , logout_user , login_required


class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/")
def home():
    tmp = models.get_sample()
    return render_template(
        "home.html",
        title="My Books !",
        books=tmp)

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template(
    "login.html",
    form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/book/<id>")
def book(id):
    books = models.get_book(id)
    return render_template(
        "book.html",
        book=books)

@app.route("/author/<id>")
def author(id):
    author = models.get_author(id)
    books = models.get_book_by_author(id)
    return render_template(
        "author.html",
        author=author,books=books)


@app.route("/edit")
@login_required
def edit():
    return render_template(
        "edit.html")

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = models.get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit_author.html",
        author=a, form=f)


@app.route("/save/author/", methods=("POST",))
@login_required
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = models.get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("author", id=a.id))
    a = models.get_author(int(f.id.data))
    return render_template(
        "edit_author.html",
        author=a, form=f)
