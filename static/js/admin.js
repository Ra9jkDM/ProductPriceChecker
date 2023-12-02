import { getPath } from "./modules/configLoader.js";
import { getJSON } from "./modules/loadJson.js"

const users_api = getPath("/api/users");
const save_user = getPath("/api/save_user");
const delete_user = getPath("/api/delete_user");

const attributes = ["email", "passwd", "firstname", "lastname", "role", "is_active" ]



getJSON(users_api).then(function(data) {
    console.log(data);
    let table = document.getElementById("users-list");
    console.log(table);
    let tmp = create_users(data["users"], data["roles"], table)
    console.log(tmp);
});


function create_user(user, roles) {
	let tr = document.createElement("tr");
	
	attributes.forEach((element) => {
		let td = document.createElement("td");
        
        if (element == "is_active") {
            td.innerHTML = user[element] ? "Да": "Нет";
        }
        else if (element == "passwd"){
            td.innerHTML = "*****";
        }
        else if (element == "role"){
            td.innerHTML = roles.find((e)=> e["id"] == user[element])["name"] == "User" ? "Пользователь": "Админ";
        }
        else {
		    td.innerHTML = user[element];
        }
		tr.appendChild(td);}
	);
	
	/* add Buttons */
	let td_save = create_button("Сохранить", "button save", save_user);
    let td_delete = create_button("Удалить", "button delete", delete_user);

	tr.appendChild(td_save);
	tr.appendChild(td_delete);
	
	return tr;
}

function create_button(name , class_name, href) {
    let td = document.createElement("td");
	td.setAttribute("class", "ignore");
	
	let div = document.createElement("div");
	div.setAttribute("class", class_name);
	div.innerHTML = name;
	
	let a = document.createElement("a");
	a.href = href;
	a.appendChild(div);
	td.appendChild(a);

    return td;
}

function create_users(users, roles, table) {
	for (let i=0; i<users.length; i++) {
		table.appendChild(create_user(users[i], roles));
	}
	
}

