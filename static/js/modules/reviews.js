import { getJSON, sendJSON, sendForm } from "./load_json.js";

const image = "/img/trash.png";
const api_url = "/api/delete_comment"

const id = document.getElementById("id").innerText;
const current_user_id = document.getElementById("user_id").innerText;
const is_admin = (document.getElementById("is_admin").innerText == "True");
const text = document.getElementById("new-review");
const base_reviews = document.getElementById("reviews");


export function createReviews(reviews){
    for(let i=0; i < reviews.length; i++) {
        let review = _createReview(reviews[i].id, reviews[i].user_id, reviews[i].name, reviews[i].description);
        base_reviews.appendChild(review);
    }
}


export function createNewReview() {
    if(text.value !== ''){
        let data = {
            "product_id":id,
            "comment": text.value,
        };
        sendJSON("/api/add_comment", data).then(function(d) {
            let review = _createReview(d.id, current_user_id, d.name, data.comment);
            base_reviews.appendChild(review);
            text.value = "";
        })
    }
}

function deleteReview() {
    const element = this.parentElement.parentElement;
    const id = element.getElementsByClassName("id")[0].innerText;
    console.log("id: ", id);

    sendJSON(api_url, {"id": id}).then(function(r) {
        if(r.status == "ok"){
            element.remove();
        }
    });
}

function _createReview(comment_id, user_id, user_name, user_desc) {
    const review = document.createElement("div");
    review.setAttribute("class", "review");

    const id = document.createElement("div");
    id.setAttribute("class", "id");
    id.style = "display: none;";
    id.textContent = comment_id;

    const name = document.createElement("div");
    name.setAttribute("class", "name");
    name.textContent = user_name;

    if (user_id == current_user_id || is_admin) {
        const img = document.createElement("img");
        img.src = image;
        img.onclick = deleteReview;
        name.appendChild(img);
    }

    const desc = document.createElement("div");
    desc.setAttribute("class", "description");
    desc.textContent = user_desc;

    review.appendChild(id);
    review.appendChild(name);
    review.appendChild(desc);

    
    return review;
}