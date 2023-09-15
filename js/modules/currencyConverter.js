const after_dot = 2;


export function getRubPrice(price) {
    return price + " ₽"
}
export function getDolPriceNumber(price, dollar) {
    const round_num = Math.pow(10, after_dot);

    let result = Math.round(price*round_num / dollar)/round_num;
    
    return result;
}

export function getDolPrice(price, dollar) {
    let result = getDolPriceNumber(price, dollar);
    let str = result.toString();
    let dot_index = str.indexOf('.');

    if (dot_index != -1) {
        str += '0'.repeat(after_dot - (str.length - 1 - dot_index));
    } else {
        str += '.'+'0'.repeat(after_dot);
    }

    return str + " $";

}
