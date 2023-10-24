const INFINITY = -1

export function sortProductsByASC(products){
    return products.sort(function(a, b) {
        if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        }
        return 0;
    })
}
export function sortProductsByDESC(products){
    return products.sort(function(a, b) {
        if (a.name < b.name) {
            return 1;
        } else if (a.name > b.name) {
            return -1;
        }
        return 0;
    })
}

export function sortProductsByPriceASC(products){
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

export function sortProductsByPriceDESC(products){
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

export function sortProductPrices(products) {
    for(const product of products) {
        product.prices.sort(function(a, b) {
            a = a.price;
            b = b.price;

            if (a == INFINITY){
                return 1;
            } else if (b == INFINITY) {
                return -1;
            }

            if (a > b) {
                return 1;
            } else if (a< b) {
                return -1;
            }
            return 0;
        });
    }
}

export function sortDatasetsByLengthASC(input){
    return input.sort(function(a, b) {
        let len = a.data.length - 1;
        if (a.data[len] > b.data[len]) {
            return 1;
        } else if (a.data[len] < b.data[len]) {
            return -1;
        }
        return 0;
    });
}

export function sortShopsByPriceDESC(a, b) {
    a = a.price;
    b = b.price;

    if (a == INFINITY){
        return 1;
    } else if (b == INFINITY) {
        return -1;
    }

    if (a > b ) {
        return 1;
    } else if (a < b) {
        return -1;
    }
    return 0;
}