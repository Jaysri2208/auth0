import json
from os import environ as env
from urllib.parse import urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, flash


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out", "success")
    return redirect(url_for("home"))

    


@app.route("/")
def home():
    user_info = session.get('user', {})
    user_name = user_info.get("userinfo", {}).get("name", "Guest")
    return render_template("home.html", user_name=user_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
