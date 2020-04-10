import os, re, requests, json

from flask import Flask, session, render_template, request, url_for, redirect, flash, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from model import *

app = Flask(__name__)

# "postgres://gqcymvpxhaebxl:864842868b216a580a752e84b29ea2eaccf3051c39c856a8f18c611241ab2252@ec2-23-21-160-38.compute-1.amazonaws.com:5432/d2qoamqonbficp"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL Not Set")

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

Session(app)

db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    books = db.query(Book).filter(Book.year >= 2015).all()
    return render_template("index.html", username=session["user_name"], books=books)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    key = request.form.get("key")
    return redirect(url_for("get_search", key=key))


@app.route("/search/<string:key>")
@login_required
def get_search(key):
    result = []
    count = sum(c.isdigit() for c in key)
    books = db.query(Book).filter().all()
    for book in books:
        if count >= 5:
            if re.search(key, book.isbn):
                result.append(book)
        elif count <= 2:
            if re.search(key, book.title):
                result.append(book)
            elif re.search(key, book.author):
                result.append(book)
        elif count == 4:
            if re.search(key, str(book.year)):
                result.append(book)
    if len(result) == 0:
        abort(404)
    return render_template("search.html", books=result, length=len(result), key=key)


@app.route("/book/<string:isbn>", methods=["GET", "POST"])
@login_required
def get_book(isbn):
    review = request.form.get("review")
    rating = request.form.get("rating")
    username = session["user_name"]
    user_review = False

    if request.method == "POST":
        if not review or not rating:
            flash("You must fill all inputs to submit a review!", "danger")
        else:
            new_reviewer = Review(review=review, rating=rating, reviewer=username, book=isbn)
            db.add(new_reviewer)
            db.commit()
            flash("Your review has been submitted!", "success")

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "5Itauod8y2VYwMU89tTY5A", "isbns": isbn})
    details = res.json()['books'][0]
    average_rating = details["average_rating"]
    number_of_ratings = details["work_reviews_count"]

    book = db.query(Book).filter(Book.isbn == isbn).first()
    reviewed = db.query(Review).filter(Review.reviewer == username).all()
    for row in reviewed:
        if row.book == isbn:
            user_review = True
            break
    return render_template("book.html", book=book, review=user_review, av_rate=average_rating,
                           number_of_ratings=number_of_ratings)


@app.route("/api/<string:isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "5Itauod8y2VYwMU89tTY5A", "isbns": isbn})
    details = res.json()['books'][0]
    return details


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        # Query database for username
        user = db.query(User).filter_by(username=username).first()

        # Ensure username and password is provided
        if not username or not password:
            flash("You must fill all inputs.", "danger")
            return redirect("/login")

        # Ensure username is exist
        elif user is None:
            flash("username does not exist!", "danger")
            return redirect("/login")

        # Ensure username exists and password is correct
        elif not check_password_hash(user.password, request.form.get("password")):
            flash("Incorrect password!", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = user.id
        session["user_name"] = user.username
        # Redirect user to home page
        # return render_template("main.htm", name=session["user_name"])
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("repassword")
        email = request.form.get("email")
        if not password or not username or not email:
            flash("You must fill all inputs", "danger")
            return render_template("register.html")
        else:
            if password != re_password:
                flash("Your password doesn't match confirm password")
                return render_template("register.html")
            elif db.query(User).filter_by(username=username).first():
                flash("Sorry, username exists!", "danger")
                return render_template("register.html")
        new_user = User(username=username, password=generate_password_hash(password), email=email)
        db.add(new_user)
        db.commit()
        flash("Congratulations! you have created a new account, Login now!", "success")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
