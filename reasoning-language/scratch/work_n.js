function tally(l) {
    let m = {};
    for (const w of l) {
        if ((Array.isArray(m) ? m.includes(w) : (w in m))) {
            m = {...m, [w]: (m[w] + 1)};
        } else {
            m = {...m, [w]: 1};
        }
    }
    return m;
}
console.log(tally(["a","b","a"]))
