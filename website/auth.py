from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from datetime import datetime


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Login all user types."""

    # Edge Case - return to login page if method is not POST
    if request.method != "POST":
        return render_template("login.html", user=current_user)

    # If the request method is POST, proceed with login
    email_or_username = request.form.get("email-or-username")
    password = request.form.get("password")

    # Logic for allowing users to enter username or email
    from_email = User.query.filter_by(email=email_or_username).first()
    from_username = User.query.filter_by(username=email_or_username).first()
    user = from_email if from_email else from_username

    # If user is authenticated, log them in, else flash a warning
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
        else:
            flash(f"Password entered for {email_or_username} is incorrect.", category="error")
    else:
        flash(f"There is no user account with email/username: {email_or_username}.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """Sign-up page for a standard 'Viewer' account."""

    # Edge Case - return to sign-up page if method is not POST
    if request.method != "POST":
        return render_template("signup.html", user=current_user)

    # If the request method is POST, proceed with sign-up
    # Get all the data from the form
    username = request.form.get("username")
    email = request.form.get("email")
    first_name = request.form.get("fName")
    last_name = request.form.get("lName")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    # Logic for deciding if user wants to subscribe
    subscribe = True if (request.form.get("subscribe") == "subscribe") else False

    # Objects to check for edge cases
    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    # Check for edge cases and if none, create the new user
    if email_exists:
        flash("Email is already in use!", category="error")
    elif username_exists:
        flash("Username is already in use!", category="error")
    elif not first_name or not last_name:
        flash("You must enter a First and Last name!")
    elif password1 != password2:
        flash("Passwords do not match!", category="error")
    elif len(username) < 2:
        flash("Username is too short!", category="error")
    elif len(password1) < 6:
        flash("Password is too short!", category="error")
    else:
        new_user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash(password1, method="sha256"),
            date_created=datetime.now(),
            permissions="Viewer",
            subscribed=subscribe,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/sign-up-root", methods=["GET", "POST"])
def sign_up_root():
    """Sign-up page for a 'Root' account. Route hidden."""

    # Edge Case - return to sign-up page if method is not POST
    if request.method != "POST":
        return render_template("signup.html", user=current_user)

    # If the request method is POST, proceed with sign-up
    # Get all the data from the form
    username = request.form.get("username")
    email = request.form.get("email")
    first_name = request.form.get("fName")
    last_name = request.form.get("lName")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    # Objects to check for edge cases
    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    # Check for edge cases and if none, create the new user
    if email_exists:
        flash("Email is already in use!", category="error")
    elif username_exists:
        flash("Username is already in use!", category="error")
    elif not first_name or not last_name:
        flash("You must enter a First and Last name!")
    elif password1 != password2:
        flash("Passwords do not match!", category="error")
    elif len(username) < 2:
        flash("Username is too short!", category="error")
    elif len(password1) < 6:
        flash("Password is too short!", category="error")
    else:
        new_user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash(password1, method="sha256"),
            date_created=datetime.now(),
            permissions="Root",
            subscribed=False,  # Root users need not subscribe
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    """Log out a user. Redirect to home page."""

    logout_user()
    return redirect(url_for("views.home"))
