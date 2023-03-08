from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    """Home view."""

    # Define all posts and pass them to home template
    posts = Post.query.all()

    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    """Create a new post view."""

    # Edge Case - return to create post page if method is not POST
    if request.method != "POST":
        return render_template("create_post.html", user=current_user)

    # Define request parameters
    title = request.form.get("title")
    description = request.form.get("description") if request.form.get("description") else ""
    text = request.form.get("text")
    image = request.form.get("image") if request.form.get("image") else None

    # Edge Cases - Verify text and title parameters were passed
    if not text or not title:
        flash("Post cannot be empty!", category="error")
        return render_template("create_post.html", user=current_user)

    # Create the new post instance
    post = Post(
        title=title,
        description=description,
        text=text,
        image=image,
        author=current_user.id,
        date_created=datetime.now(),
        date_updated=datetime.now(),
    )
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("views.post", post_id=post.id))


@views.route("/edit-post/<post_id>")
@login_required
def edit_post(post_id):
    """Edit post view. Fills out the edit post form."""

    # Get the instance of the post you will edit
    post = Post.query.filter_by(id=post_id).first()

    # Edge Case - return home and warn user if the post does not exist
    if not post:
        flash("This post does not exist!", category="error")
        return render_template("home.html", user=current_user)

    # Render the edit post page with all the post's current contents filled out
    return render_template("edit_post.html", user=current_user, post=post)


@views.route("/update-post/<post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    """Update the post passed with the new info submitted."""

    # Edge Case - return home if the method is not post
    if request.method != "POST":
        return render_template(url_for("home.html"), user=current_user)

    # Get the instance of the post you will update
    post = Post.query.filter_by(id=post_id).first()

    # Edge Case - return home and warn user if the post does not exist
    if not post:
        flash("This post does not exist!", category="error")
        return render_template("home.html", user=current_user)

    # Get updated info from form
    title = request.form.get("title")
    description = request.form.get("description")
    text = request.form.get("text")
    image = request.form.get("image")

    # Edge Cases - Ensure you have the info you need
    if not (title or text or image):
        flash("All fields are required except description!", category="error")
        return render_template("home.html", user=current_user)

    # Update the post object
    post.title = title
    post.description = description
    post.text = text
    post.image = image
    post.date_updated = datetime.now()
    db.session.commit()

    return redirect(url_for("views.post", post_id=post.id))


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    """Delete a post."""

    # Get the instance of the post you will delete
    post = Post.query.filter_by(id=id).first()

    # Edge Cases - Ensure post exists & user can delete it
    if not post:
        return jsonify({"error": "Post does not exist.", "status": 400})
    if current_user.id == post.id:
        return jsonify({"error": "You do not have permission to delte this post.", "status": 401})

    # Delete post instance
    db.session.delete(post)
    db.session.commit()

    return jsonify({"success": "Post deleted successfully.", "status": 200})


@views.route("/posts")
def all_posts():
    """All posts view."""

    # Get all the posts and pass them to the posts page
    posts = Post.query.all()

    return render_template("posts.html", user=current_user, posts=posts)


@views.route("/posts/<username>")
@login_required
def posts(username):
    """View for all posts for a given user. Currently hidden."""

    # Get intance of user
    user = User.query.filter_by(username=username).first()

    # Edge Case - redirect to home page if user does not exist
    if not user:
        flash("No user with that username exists!", category="error")
        return redirect(url_for("views.home"))

    # Get user's posts and pass them to the page
    posts = user.posts

    return render_template("users_posts.html", user=current_user, posts=posts, username=username)


@views.route("/post/<post_id>")
def post(post_id):
    """Single post view."""

    # Get instance of the post you want to display andpass it to post page
    post = Post.query.filter_by(id=post_id).first()

    return render_template("post.html", user=current_user, post=post)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """Create a comment."""

    # Edge Case - If method is not post, redirect to all posts page
    if request.method != "POST":
        return redirect(url_for("views.all_posts"))

    # Get the comment and the post the comment corresponds to
    comment = request.form.get("text")
    post = Post.query.filter_by(id=post_id).first()

    # Check for edge cases - empty comment & nonexistant post
    if not comment:
        flash("Comment cannot be empty!", category="error")
        return render_template("post.html", user=current_user, post=post)
    if not post:
        return jsonify({"error": "Post does not exist!", "status": 400})

    # Write the comment to the post and refresh the page
    comment = Comment(text=comment, author=current_user.id, date_created=datetime.now(), post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return render_template("post.html", user=current_user, post=post)


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    """Delete Comment."""

    # Get instance of comment to be deleted
    comment = Comment.query.filter_by(id=comment_id).first()

    # Edge Cases - ensure comment exists and user has correct permissions
    if not comment:
        return jsonify({"error": "Comment does not exist.", "status": 400})
    if current_user.id != comment.author and current_user.id != comment.post.author:
        return jsonify({"error": "You do not have permission to delete this comment.", "status": 400})

    # Delete the comment
    db.session.delete(comment)
    db.session.commit()

    return jsonify({"success": "Comment deleted.", "status": 200})


@views.route("/like-post/<post_id>", methods=["POST"])
def like(post_id):
    """Like a Post: Create or delete like object."""

    # Initially check that user is logged in. Return error if not.
    if not current_user.is_authenticated:
        flash("You must log in to like posts!", category="error")
        return jsonify({"error": "You must log in to like posts!", "status": 401})

    # Retreive the post and like objects given the post id and current user's id
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    # Edge Case - check that the posts exists. Return error if not
    if not post:
        return jsonify({"error": "Post does not exist.", "status": 400})

    # Logic to update the like instance
    if like:
        db.session.delete(like)
    else:
        like = Like(author=current_user.id, date_created=datetime.now(), post_id=post_id)
        db.session.add(like)
    db.session.commit()

    # Return the amount of likes and bool of whether user has like the post or not.
    return jsonify(
        {"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes), "status": 200}
    )


@views.route("/pin-post/<post_id>", methods=["POST"])
@login_required
def pin(post_id):
    """Pin a Post: Toggle it's pinned status"""

    # Retreive the post and pinned instances
    post = Post.query.filter_by(id=post_id).first()
    currently_pinned = post.pinned

    # Edge Case - check that the post exists
    if not post:
        return jsonify({"error": "Post does not exist.", "status": 400})

    # Logic to update the pinned status
    post.pinned = False if currently_pinned else True
    db.session.commit()

    # Return the amount of likes and bool of whether user has like the post or not.
    return jsonify({"pinned": post.pinned, "status": 200})


@views.route("/subscribe/<user_id>")
@login_required
def subscribe(user_id):
    """Toggles a user's subscription status between True and False."""

    # Get the user instance you will be updating
    user = User.query.filter_by(id=user_id).first()

    # Check the edge case of a user not existing
    if not user:
        return jsonify({"error": "User's subscription status could not be updated", "status": 400})

    # Logic to toggle user's subscription status
    new_subscription = False if user.subscribed else True
    user.subscribed = new_subscription
    db.session.commit()

    return jsonify(
        {
            "success": f"User's subscription status updated to: {new_subscription}",
            "subscribed": new_subscription,
            "status": 200,
        }
    )
