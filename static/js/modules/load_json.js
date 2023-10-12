export async function getJSON(url) {
    const response = await fetch(url);
    return await response.json();
}

export async function sendJSON(url, json) {
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(json), 
        headers: {
                    'Accept': 'application/json',
                    "Content-type": "application/json; charset=UTF-8",
                }
        });
    return await response.json();
}

export async function sendForm(url, form) {
    const response = await fetch(url, {
        method: "POST",
        body: form, 
        headers: {   }
        });
    return await response.json();
}

