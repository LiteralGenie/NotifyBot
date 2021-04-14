function contains_all(to_search, to_find) {
    if(!Array.isArray(to_search)){
        to_search= to_search.split(/\s+/)
    }
    if(!Array.isArray(to_find)){
        to_find= to_find.split(/\s+/)
    }

    to_search= to_search.map(x => String(x).toLowerCase())
    to_find= to_find.map(x => String(x).toLowerCase())

    let ret= to_find.every(x => to_search.includes(x))

    return ret
}


export {
    contains_all
}