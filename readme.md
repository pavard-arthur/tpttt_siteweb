# Projet Web Title Plot Twister Tonic T3
# Contributors : 
### PAVARD Arthur info21A (alternance)

discovery of the flask framework with an web app 
with : 
- dominate
- itsdangerous
- MarkupSafe
- visitor
- click (cli)
- python-dotenv (because SECRET_KEY should be in the .env file)
    ### **Please generate your own keys**
    ```$uuidgen```
    for CSRF (Cross-Site Request Forgery)
- PyYAML ( yaml parser for DB import)
- Werkzeug ( the python web server)
- Jinja2 ( bootstrap html render Client-Side-Rendering)
- Flask
- Bootstrap-Flask
- flask-sqlalchemy
- flask-wtf
- flask-login
- WTForms

# To Run

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
# flask
# Commands:
#   loaddb   Creates the tables and populates them with data.
#   newuser  Adds a new user.
#   passwd   change a user passwd.
#   routes   Show the routes for the app.
#   run      Run a development server.
#   shell    Run a shell in the app context.
#   syncdb   Creates all missing tables
flask loaddb
flask run
```

# TODO
- [X] flask set up
- [X] bootstrap set up
- [X] DB set up
- [X] cli commands
    - [X] DB create
    - [X] DB load
    - [X] DB user create
    - [X] DB user load
    - [X] DB user change password
- [ ] views
    - [X] main page samples
    - [X] book
    - [X] author
    - [ ] categories
    - [ ] favorites
- [ ] edit
    - [ ] book
    - [X] author
    - [ ] categories
    - [ ] favorites
- [ ] add
    - [ ] book
    - [ ] author
    - [ ] categories
    - [ ] favorites