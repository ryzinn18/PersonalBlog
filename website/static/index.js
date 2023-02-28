function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert("Could not like post."));
  }


function delete_comment(commentId) {
    const comment = document.getElementById(`comment-${commentId}`)
  
    fetch(`/delete-comment/${commentId}`, {}) // , { method: "POST" } removed this as delete_comment takes no methods
    .then((res) => res.json())
    .then((data) => {
        if (data["success"]) {
            comment.remove();
        }
    })
    .catch((e) => alert("Could not delete comment."));
  }