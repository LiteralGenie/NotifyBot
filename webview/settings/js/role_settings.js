import { contains_all } from "/js/misc_utils.js";


// helpers
var form= document.getElementById("role-form")
var rows= Array.from(form.getElementsByClassName("role-row"))
var submit_button= form.getElementsByClassName("role-submit")[0]
ROLE_FORM.valid= false

function get_values(row) {
    let series_input= row.getElementsByClassName("series-input")[0]
    let role_input= row.getElementsByClassName("role-input")[0]

    // get input values
    let raw_series = series_input.value || series_input.placeholder
    let raw_role = role_input.value || role_input.placeholder

    // clean values
    let clean_series = raw_series.split(",").map(x => x.trim())
    let clean_role = raw_role.split(",").map(x => x.trim())

    return {
        series: clean_series,
        role: clean_role,
    }
}

function get_row_listener(row) {
    let match_label= row.getElementsByClassName("match-label")[0]

    function update() {
        function get_text() {
            // get cleaned values
            let tmp= get_values(row)
            let clean_series= tmp.series
            let clean_role= tmp.role

            // parse using data dicts
            let match_role= clean_role.map(x => ROLE_FORM.ROLES_AVAILABLE[x])
            for (let i=0; i<match_role.length; i++) {
                let role= match_role[i]
                if (role === undefined) {
                    ROLE_FORM.valid= false
                    return `Error. ${clean_role[i]} is not a valid role id.`
                }
            }

            let match_series= Object.values(ROLE_FORM.SERIES_DATA).filter( data => {
                return clean_series.every(x => contains_all(data['display_name'], x))
            })

            // text-ify
            let text_series= `[${match_series.map(x => x['display_name']).join("], [")}]`
            let text_role= `[${match_role.join("], [")}]`

            if(clean_series[0] === "all") {
                text_series= "all series"
            }
            else if(match_series.length === 0) {
                text_series= "[None] -- This is okay for new series."
            }

            let ret_1= `Series matched -- ${text_series}`
            let ret_2= `Roles matched: -- ${text_role}`

            ROLE_FORM.valid= true
            return `${ret_1}\n${ret_2}`
        }

        // update status text
        match_label.value= get_text()

        // update button clickability
        if(!ROLE_FORM.valid) {
            submit_button.innerText= "inputs invalid"
            submit_button.disabled= true
        }
        else {
            submit_button.innerText= "submit role config"
            submit_button.disabled= false
        }
    }
    return update
}

function add_row_listeners(row) {
    let series_input = row.getElementsByClassName("series-input")[0]
    let role_input = row.getElementsByClassName("role-input")[0]
    let remove_button = row.getElementsByClassName("remove-button")[0]

    // update-status listeners
    let tmp = get_row_listener(row)
    series_input.addEventListener("keyup", tmp)
    role_input.addEventListener("keyup", tmp)
    tmp()

    // remove row listener
    remove_button.addEventListener("click", e => {
        row.remove()
    })
}

function create_row() {
    let tmp= rows[rows.length-1].cloneNode(true)
    add_row_listeners(tmp)
    return tmp
    }

// form validation
for(let r of rows) {
    add_row_listeners(r)
}

// form submission
submit_button.addEventListener("click", _ => {
    rows= Array.from(document.getElementsByClassName("role-row"))
    let data= {}

    // aggregate values
    for(let r of rows) {
        // get cleaned values
        let tmp= get_values(r)
        data[tmp.series]= tmp.role
    }

    // submit
    let xhr= new XMLHttpRequest()
    xhr.open("POST", "/settings/roles", false)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify(data))

    // update form
    for(let r of rows) {
        let series_input = r.getElementsByClassName("series-input")[0]
        let role_input = r.getElementsByClassName("role-input")[0]

        series_input.placeholder= series_input.value || series_input.placeholder
        role_input.placeholder= role_input.value || role_input.placeholder

        series_input.value= ""
        role_input.value= ""
    }
})


// add-row button
let add_button= form.getElementsByClassName("add-row")[0]
add_button.addEventListener("click", e => {
    let new_row= create_row()
    form.getElementsByTagName("tbody")[0].appendChild(new_row)
})
