import {sortProductPrices, sortProductsByASC, sortProductsByDESC, sortProductsByPriceASC, sortProductsByPriceDESC} from "./modules/sorts.js"
import {getRubPrice, getDolPriceNumber, getDolPrice} from "./modules/currencyConverter.js";
import { getJSON } from "./modules/loadJson.js"
import { getPath } from "./modules/configLoader.js";

const product_api = getPath("/api/products");
const product_href = getPath("/product?id=");
const product_img = getPath("");

const currency_name = "USD";
const products = document.getElementById("products");

let json_data = "";
products.innerHTML = "";

getJSON(product_api).then(function(data) {
    json_data = data;

    sortProductPrices(json_data.products);
    sortProductsByASC(json_data.products);

    let all = createAllProducts(json_data);
    appendChildren(products, all);
})

function createAllProducts(json) {
    let blocks = []

    let currency = json.currencies.find(function (e) {
        if(e.code == currency_name) {
            return true;
        }
        return false
    });
    
    for(const product of json.products) {
        let min_price = product.prices[0].price;

        blocks.push(createProductBlock(product.product_id, product.name, 
                                        product.image, getRubPrice(min_price),
                                        getDolPrice(min_price, currency.price)));
    }
    return blocks;
}


function createProductBlock(id, name, image, price_rub, price_dol) {
    const product = document.createElement("a");
    product.setAttribute("class", "product");
    product.href = product_href + id;

    const img = document.createElement("img");
    img.setAttribute("class", "image");
    img.setAttribute("src", product_img+image);

    const name_block = document.createElement("div");
    name_block.setAttribute("class", "name");
    name_block.innerHTML = name;

    const price = document.createElement("div");
    price.setAttribute("class", "price");

    const rub = document.createElement("div");
    rub.setAttribute("class", "price-rub left");
    rub.innerHTML = price_rub;

    const dol = document.createElement("div");
    dol.setAttribute("class", "price-dol right");
    dol.innerHTML = price_dol;

    price.appendChild(rub);
    price.appendChild(dol);

    product.appendChild(img);
    product.appendChild(name_block);
    product.appendChild(price);

    return product
}

 
function appendChildren(parent, children) {
    for (const child of children) {
        parent.appendChild(child);
    }
}


document.getElementById("sort").onchange = function(e) {
    let value = e.target.value;
    
    products.innerHTML = "";

    switch(value) {
        case "nameASC":
            sortProductsByASC(json_data.products);
            break;
        case "nameDESC":
            sortProductsByDESC(json_data.products);
            break;
        case "priceASC":
            sortProductsByPriceASC(json_data.products);
            break;
        default:
            sortProductsByPriceDESC(json_data.products);
            break;
    }


    let all = createAllProducts(json_data);
    appendChildren(products, all);
};







