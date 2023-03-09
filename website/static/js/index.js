function like(postId) {
    // Invoke like-post function & update like count/icon in frontend dynamically.
  
    fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
    // If call successful...
    if (data["status"] === 200) {
        // Get like objects to be updated
        const likeButton = document.getElementById(`like-button-${postId}`);
        const likeCount = document.getElementById(`likes-count-${postId}`);
        // Update like count in html
        likeCount.innerHTML = data["likes"];
        // Toggle the like button's image
        if (data["liked"] === true) {
            likeButton.className = "fas fa-thumbs-up";
        } else {
            likeButton.className = "far fa-thumbs-up";
        }
    }
    // If unsuccessful because of permissions, redirect to login page
    if (data["status"] === 401) {
        window.location.replace("/login");
    }
    })
    // Catch any unforseen errors and throw generic alert   
    .catch((e) => alert("Could not like post."));
  }


function delete_comment(commentId) {
    // Invoke delete comment function & remove comment from frontend dynamically.
  
    fetch(`/delete-comment/${commentId}`, {}) 
    .then((res) => res.json())
    .then((data) => {
        // If invocation successful, delete the comment from page
        if (data["success"]) {
            const comment = document.getElementById(`comment-${commentId}`)
            comment.remove();
        }
    })
    // Catch any unforseen errors and throw generic alert   
    .catch((e) => alert("Could not delete comment."));
  }


function delete_post(postId) {
    // Invoke delete post view & remove post's card from frontend dynamically. 
    
    // Confirm user want's to delete post. Return if not
    const response = confirm("Are you sure you want to do delete this post?");
    if (response === false) {
        return
    }

    fetch(`/delete-post/${postId}`, {}) 
    .then((res) => res.json())
    .then((data) => {
        // If post is successfully deleted
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
    // Catch any unforseen errors and throw generic alert   
    .catch((e) => alert("Could not delete post."));
}


function pin(postId) {
    // Invoke pin function & update pin icon dynamically.
  
    fetch(`/pin-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
    // If pin updated successfully, update icon it in html
    if (data["status"] === 200) {
        const pinButton = document.getElementById(`pin-button-${postId}`);
        if (data["pinned"] === true) {
            pinButton.className = "param fa-solid fa-check";
        } else {
            pinButton.className = "param fa-solid fa-location-pin";
        }
    }
    })
    // Catch any unforseen errors and throw generic alert  
    .catch((e) => alert("Could not pin post."));
  }


function toggle_subscription(userId) {
    // Invoke subscribe function & update subscribed icon(s) dynamically.
    
    fetch(`/subscribe/${userId}`)
    .then((res) => res.json())
    .then((data) => {
        // If subscription toggled successfully, update the icons 
        if (data["status"] === 200) {
            const subscribedNavIcon = document.getElementById(`subscribed-${userId}`);
            const subscribedHomeIcon = document.getElementById(`subscribed-home-${userId}`)
            const subscribedHomeText = document.getElementById(`subscribed-text-${userId}`)
            if (data["subscribed"] === true) {
                // Always update nav icon
                subscribedNavIcon.className = "nav-item nav-link fa-solid fa-envelope";
                // Only update Home page icon if on home page
                if (subscribedHomeIcon) {
                    subscribedHomeIcon.className = "nav-item nav-link fa-solid fa-envelope fa-5x";
                    subscribedHomeText.innerHTML = "You are currently subscribed!<br>To unsubscribe, clicke the icon below..."
                }
            } else {
                // Always update nav icon
                subscribedNavIcon.className = "nav-item nav-link fa-regular fa-envelope";
                // Only update Home page icon if on home page
                if (subscribedHomeIcon) {
                    subscribedHomeIcon.className = "nav-item nav-link fa-regular fa-envelope fa-5x";
                    subscribedHomeText.innerHTML = "You are currently not subscribed!<br>Click the icon below to subscribe..."
                }
            }
        }
        // If failed, return to login page
        if (data["status"] === 400) {
            window.location.replace("/login");
        }
    })
    // Catch any unforseen errors and throw generic alert   
    .catch((e) => alert("Could not toggle subscription status."));
}