import { drawChart } from "./modules/drawChart.js";
import {getRubPrice, getDolPriceNumber, getDolPrice} from "./modules/currencyConverter.js";
import { createShopList } from "./modules/shopList.js";
import { createReviews, appendReview } from "./modules/reviews.js";


const active_color = 'wheat';
const base_color = 'white';

function sortByASC(input){
    return input.sort(function(a, b) {
        let len = a.data.length - 1;
        if (a.data[len] > b.data[len]) {
            return 1
        } else if (a.data[len] < b.data[len]) {
            return -1
        }
        return 0;
    });
}

function setMainPrice(input, len) {
    const rub = document.getElementById("price-rub");
    const dol = document.getElementById("price-dol");

    let price = input.datasets[0].data[len];
    
    rub.textContent=getRubPrice(price);
    dol.textContent=getDolPrice(price, input.dollar[data_len]);
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
        el.style.backgroundColor = active_color;
        el1.style.backgroundColor = base_color;
    } else {
        el1.style.backgroundColor = active_color;
        el.style.backgroundColor = base_color;
    }
}



let input = {
    name: "Электрочайник Hi EK-17C23",
    labels: ["12.09.2023", "13.09.2023", "14.09.2023", "15.09.2023"],
    urls: ['https://www.mvideo.ru/products/elektrochainik-hi-ek-17c23-400102164', 'http://google.com', 'http://google.com', 'http://google.com'],
    dollar: [96.5, 80, 100, 100],
    datasets: [{
        label: 'М.Видео',
        data: [2799, 3000, 2999, 2799],
        borderWidth: 1
      },
	{
        label: 'Citilink',
        data: [3020, 3500, 3200, 3400],
        borderWidth: 1
      },
      {
        label: 'Regard',
        data: [2500, 2800, 3000, 2899],
        borderWidth: 1
      },
      {
        label: 'video-shoper',
        data: [2515, 2700, 2998, 3050],
        borderWidth: 1
      }],
      reviews: [{
        name: "Bob",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque finibus hendrerit purus a dictum. Morbi quis ipsum aliquet, elementum lectus ut, venenatis nisl."
      },
      {
        name: "Alice",
        description: "Integer vel lectus et magna aliquet euismod. Nunc facilisis dui ut purus auctor"
      },
      {
        name: "Eve",
        description: "Объекты могут быть отсортированы по значению одного из своих свойств."
      }
    ]
}

function _getDollarPrice() {
    let dollar_price = structuredClone(input);
    return convertToDollarPrice(dollar_price);
}

function createListeners() {
    let rub_btn = document.getElementById('rub');
    rub_btn.addEventListener('click', changeToRuble); 

    let dol_btn = document.getElementById('dol');
    dol_btn.addEventListener('click', changeToDollar);

    let review = document.getElementById('send');
    review.addEventListener('click', appendReview);
}

input.datasets = sortByASC(input.datasets);
const data_len = input.datasets[0].data.length - 1;

let dollar_price = _getDollarPrice();

drawChart(input, 'rub-chart');
drawChart(dollar_price, 'dol-chart');

setName(input.name);
setMainPrice(input, data_len);
createShopList(input, data_len);
createReviews(input.reviews);

createListeners();


