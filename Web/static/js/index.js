import {getRubPrice, getDolPriceNumber, getDolPrice} from "./modules/currencyConverter.js";

async function getProducts(url) {
    const response = await fetch(url);
    return await response.json();
}

function createProductBlock(id, name, image, price_rub, price_dol) {
    const product = document.createElement("div");
    product.setAttribute("class", "product");
    product.setAttribute("onclick", "location.href='/product?id="+ id +"'");

    const img = document.createElement("img");
    img.setAttribute("class", "image");
    img.setAttribute("src", image);

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

function _isDollar(currency) {
    return currency.name === "Доллар";
}

function _sortProductsByASC(products){
    return products.sort(function(a, b) {
        if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        }
        return 0;
    })
}
function _sortProductsByDESC(products){
    return products.sort(function(a, b) {
        if (a.name < b.name) {
            return 1;
        } else if (a.name > b.name) {
            return -1;
        }
        return 0;
    })
}

function _sortProductsByPriceASC(products){
    return products.sort(function(a, b) {
        a = a.prices[0].price;
        b = b.prices[0].price;

        if (a > b) {
            return 1;
        } else if (a < b) {
            return -1;
        }
        return 0;
    })
}

function _sortProductsByPriceDESC(products){
    return products.sort(function(a, b) {
        a = a.prices[0].price;
        b = b.prices[0].price;

        if (a < b) {
            return 1;
        } else if (a > b) {
            return -1;
        }
        return 0;
    })
}

function _sortProductPrices(products) {
    for(const product of products) {
        product.prices.sort(function(a, b) {
            if (a.price > b.price) {
                return 1;
            } else if (a.price < b.price) {
                return -1;
            }
            return 0;
        });
    }
}

function createAllProducts(json) {
    let blocks = []

    let currency = json.currencies.find(_isDollar);
    
    for(const product of json.products) {
        let min_price = product.prices[0].price;

        blocks.push(createProductBlock(product.product_id, product.name, 
                                        product.image, getRubPrice(min_price),
                                        getDolPrice(min_price, currency.price)));
    }
    return blocks;
}



function appendChildren(parent, children) {
    for (const child of children) {
        parent.appendChild(child);
    }
}





let products = document.getElementById("products");

let json = getProducts("/api/get_products")
let json_data = "";
products.innerHTML = "";


json.then(function(data) {
    json_data = data;

    _sortProductPrices(json_data.products);
    _sortProductsByASC(json_data.products);

    let all = createAllProducts(json_data);
    appendChildren(products, all);
})

document.getElementById("sort").onchange = function(e) {
    let value = e.target.value;
    
    products.innerHTML = "";

    switch(value) {
        case "nameASC":
            _sortProductsByASC(json_data.products);
            break;
        case "nameDESC":
            _sortProductsByDESC(json_data.products);
            break;
        case "priceASC":
            _sortProductsByPriceASC(json_data.products);
            break;
        default:
            _sortProductsByPriceDESC(json_data.products);
            break;
    }


    let all = createAllProducts(json_data);
    appendChildren(products, all);
};







