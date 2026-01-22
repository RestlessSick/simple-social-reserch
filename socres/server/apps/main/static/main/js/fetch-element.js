const fetch_element_by_url = async (url) => {
    let response = await fetch(url, {
        method: 'get',
    });
    let element = await document.createElement('div');

    let html = await response.text();
    element.innerHTML = html;
    return element
};

const append_element = async (container_id, element) => {
    
    await document.getElementById(container_id).appendChild(element);
    await search_for_scripts(element);
};

const fetchPaginatedElement = async (page=0, append_to_id, desired_element,  change_onload_id) => {
    if (page == 0) {
        let main = document.querySelector('main');
        let element = await fetch_element_by_url('/polls/');
    

        if (main.innerHTML.trim() == '') {
            await append_element(main.id, element)
        }
    }
    else {
        if (page != '-1') {
            let main = document.querySelector('main');
            let element = await fetch_element_by_url('/polls/?page=' + page);

            console.log(element);
            let next_page = element.querySelector('#next_page').value;
            for (let el of element.querySelectorAll(desired_element)) {
                append_element(append_to_id, el);
            }
            
            document.getElementById(change_onload_id).onclick = () => {
                fetchPaginatedElement(next_page, desired_element, change_onload_id);
            };
        }
        else {
            message('Nothing left...')
        }
    }
}