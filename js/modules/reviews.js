export function createReviews(reviews){
    const base = document.getElementById('reviews');

    for(let i=0; i < reviews.length; i++) {
        let review = _createReview(reviews[i].name, reviews[i].description);

        base.appendChild(review);
    }
}

function _createReview(user_name, user_desc) {
    const review = document.createElement("div");
    review.setAttribute("class", "review");

    const name = document.createElement("div");
    name.setAttribute("class", "name");
    name.textContent = user_name;

    const desc = document.createElement("div");
    desc.setAttribute("class", "description");
    desc.textContent = user_desc;

    review.appendChild(name);
    review.appendChild(desc);

    return review;
}

export function appendReview() {
    const text = document.getElementById("new-review");
    const reviews = document.getElementById("reviews");

    if(text.value !== '') {
        var review = _createReview('Bot1', text.value);
        reviews.appendChild(review);
        text.value = "";
    } 
}