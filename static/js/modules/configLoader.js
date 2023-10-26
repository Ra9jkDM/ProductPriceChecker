
export const config = loadConfig();
console.log(config);

export function getPath(url) {
	return config.prefix + url;
}

export function getUserId() {
	return config.user_id;
}

export function getProductId() {
	return config.product_id;
}

export function getRole() {
	return config.is_admin;
}

function loadConfig() {
	let config = {};

	const info = document.getElementById('system-info');

	const elements = info.getElementsByTagName("div");
	for (let i=0; i<elements.length; i++) {
		let key = elements[i].id;
		let value = elements[i].innerHTML;
		if (key.startsWith("is_")) {
			config[key] = (value == "True");
		}
		else {
			config[key] = value;
		}
	}

	return config;
}



