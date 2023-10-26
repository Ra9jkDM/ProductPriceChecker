import { drawChart } from "./modules/drawChart.js";
import {getRubPrice, getDolPriceNumber, getDolPrice} from "./modules/currencyConverter.js";
import { createShopList } from "./modules/shopList.js";
import { createReviews, createNewReview } from "./modules/reviews.js";
import {getJSON} from "./modules/loadJson.js";
import {sortDatasetsByLengthASC} from "./modules/sorts.js";
import { getPath, getProductId } from "./modules/configLoader.js";


const product_api = getPath("/api/product?id=");
const product_img = getPath("");
const id = getProductId();


getJSON(product_api + id).then(function(input) {
    console.log(input);
    input.datasets = sortDatasetsByLengthASC(input.datasets);
    const data_len = input.datasets[0].data.length - 1;
    
    let dollar_price = _getDollarPrice(input);

    drawChart(input, 'rub-chart');
    drawChart(dollar_price, 'dol-chart');

    //input.urls =
    createShopList(input, data_len);
    setName(input.name);
    console.log(input);
    setMainPrice(input, data_len);
    setDescription(input.description);
    setImage(input.image);

    

    console.log(input.reviews)
    createReviews(input.reviews);

    createListeners();

})


function setMainPrice(input, len) {
    const rub = document.getElementById("price-rub");
    const dol = document.getElementById("price-dol");

    let price = input.urls[0].price;
    
    rub.textContent=getRubPrice(price);
    dol.textContent=getDolPrice(price, input.dollar[len]);
}

function setName(name) {
    const product_name = document.getElementById("name");
    product_name.textContent = name;
}

function convertToDollarPrice(prices) {
    let dollar = prices.dollar;
    let money = prices.datasets;

    for(let i = 0; i < money.length; i++) {
        for(let j = 0; j < money[i].data.length; j++) {
            money[i].data[j] = getDolPriceNumber(money[i].data[j],dollar[j]);
        }
    }

    return prices;
}

function changeToDollar() {
    _change(-1);
}
function changeToRuble() {
    _change(1);
}
function _change(num){
    const chart = document.getElementById('rub-chart');
    chart.style.zIndex = num;

    const el = document.getElementById("rub");
    const el1 = document.getElementById("dol");

    if(num > 0) {
        el.setAttribute("class", "active-button");
        el1.setAttribute("class", "");
    } else {
        el1.setAttribute("class", "active-button");
        el.setAttribute("class", "");
    }
}


function _getDollarPrice(input) {
    let dollar_price = structuredClone(input);
    return convertToDollarPrice(dollar_price);
}

function createListeners() {
    let rub_btn = document.getElementById('rub');
    rub_btn.addEventListener('click', changeToRuble); 

    let dol_btn = document.getElementById('dol');
    dol_btn.addEventListener('click', changeToDollar);

    let review = document.getElementById('send');
    review.addEventListener('click', createNewReview);
}

function setDescription(desc) {
    document.getElementById("product-description").innerHTML="<pre>" + desc + "</pre>";
}

function setImage(img) {
    document.getElementById("img").src = product_img + img;
}




