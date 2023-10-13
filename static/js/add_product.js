import { getJSON, sendJSON, sendForm } from "./modules/load_json.js";
import { parseCookie } from "./modules/parseCookies.js";
import { getRubPrice, getDolPrice } from "./modules/currencyConverter.js";


let upload_data = []
let file = null;

const is_edit = document.getElementById("id").innerHTML;

const img = document.getElementById("img");
const name = document.getElementById("name");
const description = document.getElementById("description");

console.log(is_edit);
if (is_edit != -1) {
    console.log("Edit");

    getJSON("/api/product?id="+ is_edit).then(function(input) {
        console.log(input);

        // Upload img
        img.src = input.image;
        fetch(input.image)
        .then(res => res.blob())
        .then(blob => {
            let upload_img = new File([blob], _get_image_name(input.image))
                console.log(upload_img);
                file = upload_img;
            });

        name.value = input.name;
        description.value = input.description;

        for (let i=0; i<input.urls.length; i++) {
            let url = input.urls[i];
            document.querySelector('input[alt="'+url.name+'"]').value = url.url;
            // document.querySelector('input[alt="Citilink"]')
        }
        
    });

}

function _get_image_name(path) {
    return path.split('/').slice(-1);
}


function collect_data() {
    let urls = document.getElementsByClassName("url");
    let shops = []
    for (let i of urls) {
        let child = i.children[0];
        shops.push({"name": child.alt, "url": child.value});
    }
    
    let data = {
        "name": name.value,
        "description": description.value,
        "urls": shops
    };

    return data;
}

function enable_button(){
    let save = document.getElementById("save");
    save.setAttribute("class", "button");
}

function createRow(shop, name, price, dollar) {
    console.log(shop, name, price);
    let tr = document.createElement("tr");

    let shop_name = document.createElement("td");
    shop_name.innerHTML = shop;

    let product_name = document.createElement("td");
    product_name.setAttribute("class", "name");
    product_name.innerHTML = name;

    let rub_price = document.createElement("td");
    rub_price.setAttribute("class", "price");
    rub_price.innerHTML = getRubPrice(price);

    let dol_price = document.createElement("td");
    dol_price.setAttribute("class", "price");
    dol_price.innerHTML = getDolPrice(price, dollar);

    tr.appendChild(shop_name);
    tr.appendChild(product_name);
    tr.appendChild(rub_price);
    tr.appendChild(dol_price);

    return tr;
}




let upload = document.getElementById("upload");
upload.onchange = function() {
    if (this.files && this.files[0]) {

        img.onload = () => {
            URL.revokeObjectURL(img.src)
        };

        file = this.files[0];
        img.src = URL.createObjectURL(this.files[0]);
    }
};


// ToDo change /proxy/dollar to /proxy/currency&code=USD
let check = document.getElementById("test");
check.onclick = function() {
    let data = collect_data();
    sendJSON("/proxy/shops", data).then(function(e) {
        console.log(e);
        upload_data = e;
        getJSON("/proxy/dollar").then(function(d) {
            console.log(d);
            let table = document.getElementById("shops-table");
            table.innerHTML = "";
            for (let i of e.shops) {
                let row = createRow(i.shop, i.name, i.price, d.price)
                table.appendChild(row);
            }

            enable_button();
        })
        
    });
    

    
};

let save = document.getElementById("save");
save.onclick = function() {
    console.log("Save");
    let data = collect_data();

    let prices = []


    for (let i of data.urls) {
        let price_data = upload_data.shops.filter((x)=>x.shop==i.name)[0];
        if (price_data != undefined){
            prices.push({"name": i.name, "url": i.url, 
                    "price": price_data.price});
    
        }
    }
    
    let json = {"id": is_edit, "name": data.name, "description": data.description,
                 "urls": prices, "image": file};
    console.log(json);

    let formData = new FormData();
    formData.append("image", file);
    formData.append("data", new Blob([JSON.stringify(json)], {'type': "application/json"}));

    console.log(formData, file);
    sendForm("/api/product", formData).then(function(e) {
        console.log(e);

        if (e.status == "error") {
            alert("Возникла ошибка при добавлении продукта.");
        } else {
            window.location = '/';
        }
    });
};
