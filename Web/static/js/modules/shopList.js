import {getRubPrice, getDolPriceNumber, getDolPrice} from "./currencyConverter.js";

export function createShopList(input, len){
    const shops = document.getElementById('shops');

    // let data =  input.datasets;
    let urls = input.urls.sort(function(a, b) {
        a = a.price;
        b = b.price;

        if (a > b) {
            return 1;
        } else if (a < b) {
            return -1;
        }
        return 0;
    });

    for(const shop_info of urls){
        const shop = document.createElement("div");
        shop.setAttribute('class', 'shop');
        shop.setAttribute('onclick', 'window.open("'+shop_info.url+'","Shop");');

        const name = document.createElement("div");
        name.setAttribute('class', 'name');
        name.textContent = shop_info.name;


        const prices = document.createElement("div");
        prices.setAttribute('class', 'price');

        const rub = document.createElement("div");
        rub.setAttribute('id', 'price-rub');
        rub.textContent = getRubPrice(shop_info.price);
        const dol = document.createElement("div");
        dol.setAttribute('id', 'price-dol');
        dol.textContent = getDolPrice(shop_info.price, input.dollar[len]);

        prices.appendChild(rub);
        prices.appendChild(dol);

        shop.appendChild(name);
        shop.appendChild(prices);

        shops.appendChild(shop);
    }
}

