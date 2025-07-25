// for the infinite scroll
let currentPage = 1;
let isLoading = false;
let hasMoreTweets = true;

function handleScroll() {
    if (isLoading || !hasMoreTweets) return;

    const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    if (nearBottom) {
        loadMoreTweets();
    }
}

window.addEventListener('scroll', handleScroll);

function loadMoreTweets() {
    isLoading = true;
    currentPage += 1;
    document.getElementById('loading').style.display = 'block';

    fetch(`?page=${currentPage}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('tweet-container');
            if (data.tweets.length === 0) {
                hasMoreTweets = false;
                document.getElementById('loading').style.display = 'none';
                isLoading = false;
                return;
            }

            data.tweets.forEach(tweet => {
                const tweetCard = renderTweetCard(tweet);
                container.insertAdjacentHTML('beforeend', tweetCard);
            });

            attachLikeListeners();

            if (!data.has_next) {
                hasMoreTweets = false;
            }

            document.getElementById('loading').style.display = 'none';
            isLoading = false;
        })
        .catch(err => {
            console.error('Failed to load more tweets', err);
            document.getElementById('loading').style.display = 'none';
            isLoading = false;
        });
}

function renderTweetCard(tweet) {
    return `
    <div class="col-md-6 col-lg-4 d-flex tweet-card">
        <div class="card shadow-sm border-0 flex-fill d-flex flex-column">
            <div class="card-body d-flex flex-column">
                
                <!-- Header -->
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div class="d-flex align-items-center gap-2">
                        <a href="/user/${tweet.user}/" class="text-decoration-none d-flex align-items-center gap-2">
                            <img src="${tweet.avatar_url}" alt="avatar" class="rounded-circle border" style="width: 36px; height: 36px; object-fit: cover;">
                            <h6 class="mb-1 fw-semibold text-primary mb-0">@${tweet.user}</h6>
                        </a>
                    </div>
                    <small class="text-muted">${tweet.created_at}</small>
                </div>

                <!-- Tweet Text -->
                <p class="mb-2 text-truncate-3" style="white-space: pre-wrap;">${tweet.text}</p>

                <!-- Optional Image -->
                ${tweet.photo_url ? `
                    <div class="mb-2">
                        <img src="${tweet.photo_url}" class="img-fluid rounded" style="max-height: 180px; object-fit: cover; width: 100%;" />
                    </div>
                ` : ''}

                <!-- Footer: Likes + Edit/Delete -->
                <div class="d-flex mt-auto">
                    <div class="like-section w-33 flex-fill text-end pe-1" data-tweet-id="${tweet.id}">
                        <button type="button" class="btn btn-sm like-btn w-100 ${tweet.liked ? 'btn-danger' : 'btn-outline-danger'}">
                            ❤️ <span class="like-count">${tweet.like_count}</span>
                        </button>
                    </div>

                    ${tweet.is_owner ? `
                        <div class="w-33 flex-fill px-1">
                            <a href="/tweet/${tweet.id}/edit/" class="btn btn-sm btn-outline-primary w-100">Edit</a>
                        </div>
                        <div class="w-33 flex-fill ps-1">
                            <a href="/tweet/${tweet.id}/delete/" class="btn btn-sm btn-outline-danger w-100">Delete</a>
                        </div>
                    ` : `
                        <div class="w-33 flex-fill px-1">
                            <button class="btn btn-sm w-100 invisible">Edit</button>
                        </div>
                        <div class="w-33 flex-fill ps-1">
                            <button class="btn btn-sm w-100 invisible">Delete</button>
                        </div>
                    `}
                </div>
            </div>
        </div>
    </div>
    `;
}



// Function to attach like button event listeners
function attachLikeListeners() {
    document.querySelectorAll(".like-btn").forEach(button => {
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });

    // Attach new listeners to all like buttons
    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", function () {
            const parent = button.closest(".like-section");
            const tweetId = parent.dataset.tweetId;
            const likeCountSpan = parent.querySelector(".like-count");

            fetch(`/${tweetId}/like/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => {
                    if (response.status === 403 || response.redirected) {
                        window.location.href = "/accounts/login/?next=" + window.location.pathname;
                        return null;
                    }

                    const contentType = response.headers.get("content-type");
                    if (contentType && contentType.includes("application/json")) {
                        return response.json();
                    } else {
                        throw new Error("Expected JSON, got something else");
                    }
                })
                .then(data => {
                    if (!data) return;

                    likeCountSpan.textContent = data.like_count;
                    button.classList.toggle("btn-danger", data.liked);
                    button.classList.toggle("btn-outline-danger", !data.liked);
                })
                .catch(error => console.error("Error:", error));
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    attachLikeListeners();
});