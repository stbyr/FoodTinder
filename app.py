import os
import requests
import urllib.parse

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# functions for get requests to API
def req():
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        preference = db.execute("SELECT preference FROM users WHERE id = :id", id=session["user_id"])[0]['preference']

        if preference == "NULL":
            response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?number=100&apiKey={api_key}")
        else:
            response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?diet={preference}&number=100&apiKey={api_key}")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        results = response.json()
        return {
            "results": results
        }
    except (KeyError, TypeError, ValueError):
        return None


def details(id):
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")

        response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?apiKey={api_key}")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        results = response.json()
        return {
            "results": results
        }
    except (KeyError, TypeError, ValueError):
        return None


# routes 
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        lookup_result = req()
        print(lookup_result)

        # update number of dishes seen in db
        dishes_seen = db.execute("SELECT dishesSeen FROM users WHERE id = :id", id=session["user_id"])[0]['dishesSeen']
        dishes_seen += 1
        db.execute("UPDATE users SET dishesSeen = :dishesSeen WHERE id = :id", dishesSeen=dishes_seen, id=session["user_id"])

        image = lookup_result['results']['results'][dishes_seen]['image']
        title = lookup_result['results']['results'][dishes_seen]['title']

        # get id of the shown dish and information on the dish via another get request
        id = lookup_result['results']['results'][dishes_seen]['id']
        lookup_details = details(id)

        # get username
        username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])[0]['username']

        return render_template("index.html", image=image, title=title, lookup_details=lookup_details, username=username)

    except (KeyError):
        return render_template("register.html")


@app.route('/like')
def like():
    # update recipes table
    lookup_result = req()
    dishes_seen = db.execute("SELECT dishesSeen FROM users WHERE id = :id", id=session["user_id"])[0]['dishesSeen']
    id = lookup_result['results']['results'][dishes_seen]['id']
    db.execute("INSERT INTO recipes (api_id, user_id) VALUES (?, ?)", id, session["user_id"])
    return ("nothing")


@app.route("/favorites")
def favorites():
    ids = db.execute("SELECT api_id FROM recipes WHERE user_id = :user_id", user_id = session["user_id"])
    lookups = []
    for id in ids:
        lookup_details = details(id['api_id'])
        lookups.append(lookup_details)
    return render_template("favorites.html", lookup_details=lookups)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "invalid username and/or password"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    else:
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure username does not exist yet
        elif len(rows) == 1:
            return "username already taken"

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return "must provide password and confirm it"

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return "you provided two different passwords"

        # Insert new user into users table
        else:
            hashed_password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashed_password)

        # Forget any user_id
        session.clear()

        # Remember which user has logged in
        user = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/preferences")


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    if request.method == "GET":
        return render_template("preferences.html")
    else:
        diet = request.form.get("diet")
        # for option No special preference, insert NULL
        if diet == "nodiet":
            diet = "NULL"
        db.execute("UPDATE users SET preference = :preference WHERE id = :id", preference=diet, id=session["user_id"])
        return redirect("/")
