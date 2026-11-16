function item(a) {
    let b = a[0];
    for (const c of a) {
        if ((c > b)) {
            b = c;
        }
    }
    return b;
}
function sort_put(a) {
    let b = [];
    for (const c of a) {
        let d = [];
        let e = 0;
        while (((e < b.length) && !(b[e] > c))) {
            d = [...d, b[e]];
            e = (e + 1);
        }
        d = [...d, c];
        while ((e < b.length)) {
            d = [...d, b[e]];
            e = (e + 1);
        }
        b = d;
    }
    return b;
}
console.log(item([3,9,2]), sort_put([5,1,4,1,9]))
