let form_elem = document.querySelector('#search_form')
let form_input = document.querySelector('#query')
let search_bar_section = document.querySelector('#search_bar_section')
let search_results_ctnr = document.querySelector('#search_results_ctnr')

if (form_elem){
    form_elem.addEventListener('submit', ajax_search, false)
    form_input.addEventListener('keyup', write_value, false)
}

async function ajax_search(event){
    event.preventDefault()

    let query = form_input.value;

    var res = await fetch
    (`/api/search/${query}`)

    data = await res.json();
    if (data){
        render_results(data)
    }

}

function write_value(event){
    form_input.value = event.target.value
}

function render_results(data){
    let old_search_results = search_results_ctnr.querySelectorAll('.query_result')
    if (old_search_results){
        for (let result of old_search_results){
            result.remove()
        }
    }

    if (data.status=='failed'){
        let ctnr = document.createElement("div");
        ctnr.classList.add('query_result');
        search_results_ctnr.appendChild(ctnr);

        let failed_query = document.createElement("p");
        let failed_text = document.createTextNode("nothing found");

        failed_query.appendChild(failed_text)
        ctnr.appendChild(failed_query)
        return
    }

    for (let elem of data){
        let ctnr = document.createElement("div")
        ctnr.classList.add('query_result')
        search_results_ctnr.appendChild(ctnr)

        let model_id = document.createElement("p")
        let id_text = document.createTextNode(`${elem._id}`)
        model_id.appendChild(id_text)
        
        let model_category = document.createElement("p")
        let category_text = document.createTextNode(`${elem.category}`)
        model_category.appendChild(category_text)
        
        ctnr.appendChild(model_id)
        ctnr.appendChild(model_category)

        
    }
}
