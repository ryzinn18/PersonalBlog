from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_username = request.form.get("email-or-username")
        password = request.form.get("password")

        # Logic for allowing users to enter username or email
        from_email = User.query.filter_by(email=email_or_username).first()
        from_username = User.query.filter_by(username=email_or_username).first()
        user = from_email if from_email else from_username

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
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("fName")
        last_name = request.form.get("lName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        subscribe = True if (request.form.get("subscribe") == "subscribe") else False

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

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
                subscribed=subscribe,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/sign-up-root", methods=["GET", "POST"])
def sign_up_root():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("fName")
        last_name = request.form.get("lName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

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
                permissions="Root",
                subscribed=False,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User Created!")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/subscribe/<user_id>")
@login_required
def subscribe(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user:
        new_subscribption = False if user.subscribed else True
        user.subscribed = new_subscribption
        db.session.commit()

        return jsonify(
            {
                "success": f"User's subscription status updated to: {new_subscribption}",
                "subscribed": new_subscribption,
                "status": 200,
            }
        )
    else:
        return jsonify({"error": "User's subscription status could not be updated", "status": 400})


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
