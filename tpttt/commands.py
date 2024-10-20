from .models import Author, Book, Genre
import yaml
import click
from .app import app, db
from .models import User
from hashlib import sha256


@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Creates the tables and populates them with data."""
    # création de toutes les tables
    db.create_all()

    # chargement de notre jeu de données
    books = yaml.safe_load(open(filename))

    # import des modèles
    # première passe: création de tous les auteurs
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(A_name=a)
            db.session.add(o)
            authors[a] = o

    # Ajout de la catégorie "Uncategorized"
    default_Genre = Genre(C_name="Uncategorized")
    db.session.add(default_Genre)
    db.session.commit()

    # deuxième passe: création de tous les livres
    for b in books:
        a = authors[b["author"]]
        o = Book(B_price=b["price"],
                 B_title=b["title"],
                 B_url=b["url"],
                 B_img=b["img"],
                 author=a,
                 genre=default_Genre)  # Assign default Genre
        db.session.add(o)

    # add default user
    m = sha256()
    m.update(str("passwd").encode())
    u = User(U_username="admin", U_password=m.hexdigest())
    db.session.add(u)
    db.session.commit()


@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    """Adds a new user."""
    m = sha256()
    m.update(password.encode())
    u = User(U_username=username, U_password=m.hexdigest())
    db.session.add(u)
    db.session.commit()


@app.cli.command()
@click.argument('username')
@click.argument('password')
def passwd(username, password):
    """change a user passwd."""
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    x = User.query.get(username)
    x.password = m.hexdigest()
    db.session.commit()
