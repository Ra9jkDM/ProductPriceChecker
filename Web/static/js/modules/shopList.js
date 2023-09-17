import {getRubPrice, getDolPriceNumber, getDolPrice} from "./currencyConverter.js";

export function createShopList(input, len){
    const shops = document.getElementById('shops');

    let data =  input.datasets;
    let urls = input.urls;

    for(var i=0; i<data.length;i++){
        const shop = document.createElement("div");
        shop.setAttribute('class', 'shop');
        shop.setAttribute('onclick', 'window.open("'+urls[i]+'","Shop");');

        const name = document.createElement("div");
        name.setAttribute('class', 'name');
        name.textContent = data[i].label;


        const prices = document.createElement("div");
        prices.setAttribute('class', 'price');

        const rub = document.createElement("div");
        rub.setAttribute('id', 'price-rub');
        rub.textContent = getRubPrice(data[i].data[len]);
        const dol = document.createElement("div");
        dol.setAttribute('id', 'price-dol');
        dol.textContent = getDolPrice(data[i].data[len], input.dollar[len]);

        prices.appendChild(rub);
        prices.appendChild(dol);

        shop.appendChild(name);
        shop.appendChild(prices);

        shops.appendChild(shop);
    }
}

