import os.path
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY","1234")
bootstrap = Bootstrap5(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))


app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + mkpath('../myapp.db'))

db = SQLAlchemy(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
