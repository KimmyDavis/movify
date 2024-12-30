# standard
import json
import os
import sqlite3

# third-party
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, json
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
) 
from oauthlib.oauth2 import WebApplicationClient
import requests
from werkzeug.security import generate_password_hash, check_password_hash

# internal
from db import init_db_command
from user import User
import watchlist as List_Item
from movies import trending, get_image, get_list, search_any, search_by_id, get_credits, get_related_list, get_images


# configuration
load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# custom filters
app.jinja_env.filters["get_image"] = get_image

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 google client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from the db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# JSON requests
@app.route("/movie/toggle_movie")
def toggle_movie():
    movie_id = request.args.get("movie_id")
    watchlist = List_Item.get_list(current_user.id)
    if watchlist and int(movie_id) in watchlist:
        List_Item.remove_item(current_user.id, movie_id)
    else:
        List_Item.create(current_user.id, movie_id)
    watchlist = List_Item.get_list(current_user.id)
    return json.dumps({"message": watchlist})

@app.route("/movie/watchlist")
def watchlist():
    if current_user.is_authenticated:
        watchlist = List_Item.get_list(current_user.id)
        if not watchlist:
            return {"message": "watchlist is empty"}
        return json.dumps({"message": watchlist})
    else:
        return json.dumps({"message": {}})





# Other requests

@app.route("/")
def index():
    if current_user.is_authenticated:
        trending_movies, success = trending()
        popular_movies, success2 = get_list("popular")
        top_rated_movies, success3 = get_list("top_rated")
        now_playing_movies, success4 = get_list("now_playing")
        upcoming_movies, success5 = get_list("upcoming")
        if not success:
            return render_template("apoplogy.html", message=trending_movies)
        if not success2:
            return render_template("apoplogy.html", message=popular_movies)
        if not success3:
            return render_template("apoplogy.html", message=top_rated_movies)
        if not success4:
            return render_template("apoplogy.html", message=now_playing_movies)
        if not success5:
            return render_template("apoplogy.html", message=upcoming_movies)
        return render_template("index.html", user=current_user, trending_movies=trending_movies, popular_movies=popular_movies, top_rated_movies=top_rated_movies, now_playing_movies=now_playing_movies, upcoming_movies=upcoming_movies)
    else:
        return redirect(url_for("login_normal"))
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form.get("username")
    password = request.form.get("password") 
    password2 = request.form.get("password2")
    if not (username and password and password2):
        return "all fields are required!"
    if password != password2:
        return "passwords do not match!"
    if len(password) < 5:
        return "password must be at least 5 characters long!"
    password_hash = generate_password_hash(password)

    if User.get_name(username):
        return "user already exists!"
    
    User.create("", username, "", "", password_hash)

    return redirect(url_for("login_normal"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login/normal", methods=["GET", "POST"])
def login_normal():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    if not (username and password):
        return "all fields are required!"
    user = User.get_name(username)
    if not user:
        return "user does not exist!"
    if not check_password_hash(user.password, password):
        return "incorrect password!"
    login_user(user)
    return redirect(url_for("index"))


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, password=""
    )

    # Doesn't exist? Add it to the database.
    if not User.get_name(users_name):
        User.create(unique_id, users_name, users_email, picture, "")

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for("login_normal"))
    if request.method == "GET":
        category, query = request.args.get("category"), request.args.get("query")
        results = search_any(query, cat=category)[0]
        return render_template("search.html", results=results, category=category, query=query)

@app.route("/details")
def details():
    if not current_user.is_authenticated:
        return redirect(url_for("login_normal"))
    id = request.args.get("id")
    movie_details = search_by_id(id)[0]
    credits = get_credits(id)[0]
    related_movies = get_related_list(id)[0]
    images = get_images(id)[0][:10]
    return render_template("details.html", movie_details=movie_details, credits=credits, related_movies=related_movies, images=images)

@app.route("/show-watchlist")
def show_watchlist():
    if not current_user.is_authenticated:
        return redirect(url_for("login_normal"))
    watchlist = List_Item.get_list(current_user.id)
    if not watchlist:
        return "watchlist is empty"
    watchlist_movies = [search_by_id(movie_id)[0] for movie_id in watchlist]
    return render_template("watchlist.html", watchlist_movies=watchlist_movies)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(ssl_context="adhoc")
    # app.run(debug=True)