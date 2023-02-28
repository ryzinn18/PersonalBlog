from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()

    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Post cannot be empty!", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        return jsonify({"error": "Post does not exist.", "status": 400})
    elif current_user.id == post.id:
        return jsonify({"error": "You do not have permission to delte this post.", "status": 400})
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!", category="success")

    return jsonify({"success": "Post deleted successfully.", "status": 200})


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with that username exists!", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty!", category="error")
        # return jsonify({"error": "Comment cannot be empty!", "status": 400})
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist!", category="error")
            # return jsonify({"error": "Post does not exist!", "status": 400})

    return redirect(url_for("views.home"))
    # return jsonify({"text": text, "comment_id": comment.id, "status": 200})


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        return jsonify({"error": "Comment does not exist.", "status": 400})
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        return jsonify({"error": "You do not have permission to delete this comment.", "status": 400})
    else:
        db.session.delete(comment)
        db.session.commit()

    return jsonify({"success": "Comment deleted.", "status": 200})


@views.route("/like-post/<post_id>", methods=["POST"])
def like(post_id):
    # Initially check that user is logged in. Return error if not.
    if not current_user.is_authenticated:
        flash("You must log in to like posts!", category="error")
        return jsonify({"error": "You must log in to like posts!", "status": 401})

    # Retreive the post and like objects given the post id and current user's id
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    # Check that the posts exists. Return error if not.
    if not post:
        return jsonify({"error": "Post does not exist.", "status": 400})

    # Update the like count.
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # Return the amount of likes and bool of whether user has like the post or not.
    return jsonify(
        {"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes), "status": 200}
    )
