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
    // Confirm user want's to delete post. Return if not.
    const response = confirm("Are you sure you want to do delete this post?");
    if (response === false) {
        return
    }

    // Call to delete post
    fetch(`/delete-post/${postId}`, {}) 
    .then((res) => res.json())
    .then((data) => {
    // Handle call response
        if (data["status"] == 200) {
            // Define post card element
            const postCard = document.getElementById(`post-card-${postId}`)
            // If you're on a post card page, remove the card.
            if (postCard) {
                postCard.remove();
            }
            // If you're not on a post card page, redirect to home.
            else {
                window.location.replace("/");
            }
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
// function post_comment(postId) {
//     const post = document.getElementById(`post-${postId}`)

//     // var request = new XMLHttpRequest()
//     // request.open("POST", `/create-comment/${postId}`)

//     fetch(`/create-comment/${postId}`, { method: "POST" })
//     .then((res) => res.json())
//     .then((data) => {
//         console.log(data)
//         if (data["status"] == 200) {
//             const commentCard = document.getElementById(`comments-${postId}`)
//             const commentId = data["id"];
//             const commentText = data["text"];
//             const commentAuthor = data["author"];
            
//             // Individual Comment
//             const commentDiv = document.createElement('div');
//             commentDiv.className("d-flex justify-content-between align-items-center");
//             commentDiv.setAttribute("id", commentId);
//             // Comment Author & Text
//             const textDiv = document.createElement('div');
//             const textText = document.createTextNode(commentAuthor + ": " + commentText);
//             textDiv.appendChild(textText);
//             // Insert rest of comment body here
            
//             commentDiv.appendChild(textDiv);
//             commentCard.appendChild(commentDiv)
//         } else {
//             alert(data["error"])
//         }
//     })
//     .catch((e) => alert("Could not post comment."));
//   }