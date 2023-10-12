import { getJSON, sendJSON, sendForm } from "./load_json.js";

const id = document.getElementById("id").innerText;
const text = document.getElementById("new-review");
const reviews = document.getElementById("reviews");

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

export function createNewReview() {
    if(text.value !== ''){
        let data = {
            "product_id":id,
            "comment": text.value,
        };
        sendJSON("/api/add_comment", "123", data).then(function(d) {
            let review = _createReview(d.name, data.comment);
            reviews.appendChild(review);
            text.value = "";
        })
    }
}

export function appendReview() {
    if(text.value !== '') {
        let review = _createReview('Bot1', text.value);
        reviews.appendChild(review);
    } 
}