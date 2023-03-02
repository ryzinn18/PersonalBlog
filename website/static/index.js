function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        if (data["status"] === 200) {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className = "fas fa-thumbs-up";
            } else {
                likeButton.className = "far fa-thumbs-up";
            }
        }
        if (data["status"] === 401) {
            window.location.replace("/login");
        }
      })
      .catch((e) => alert("Could not like post."));
  }


function delete_comment(commentId) {
    const comment = document.getElementById(`comment-${commentId}`)
  
    fetch(`/delete-comment/${commentId}`, {}) 
    .then((res) => res.json())
    .then((data) => {
        if (data["success"]) {
            comment.remove();
        }
    })
    .catch((e) => alert("Could not delete comment."));
  }


function delete_post(postId) {
    const response = confirm("Are you sure you want to do delete this post?");
    if (response === false) {
        return
    }

    const post = document.getElementById(`post-${postId}`)
    const postCard = document.getElementById(`post-card-${postId}`)
  
    fetch(`/delete-post/${postId}`, {}) 
    .then((res) => res.json())
    .then((data) => {
        
        if (data["status"] == 200) {
            console.log(data)
            postCard.remove();
        }
    })
    .catch((e) => alert("Could not delete post."));
  }


function pin(postId) {
    const pinButton = document.getElementById(`pin-button-${postId}`);
  
    fetch(`/pin-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        if (data["status"] === 200) {
            // pinned.innerHTML = data["pinned"];
            if (data["pinned"] === true) {
                pinButton.className = "param fa-solid fa-check";
            } else {
                pinButton.className = "param fa-solid fa-location-pin";
            }
        }
      })
      .catch((e) => alert("Could not pin post."));
  }


//   Not currently opperational
function post_comment(postId) {
    const post = document.getElementById(`post-${postId}`)
  
    fetch(`/create-comment/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
        console.log(data)
        if (data["text"]) {
            const commentId = data["comment_id"];
            const commentDiv = document.createElement('div');
            commentDiv.setAttribute("id", commentId);
            commentDiv.className("d-flex justify-content-between align-items-center");
            const newContent = document.createTextNode("Hi there and greetings!");
            commentDiv.appendChild(newContent);
            const currentDiv = document.getElementById((commentId - 1));
            document.body.insertBefore(newDiv, currentDiv);
        }
    })
    .catch((e) => alert("Could not post comment."));
  }