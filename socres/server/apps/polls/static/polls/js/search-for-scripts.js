const search_for_scripts = async (element) => {
    element.querySelectorAll('script').forEach(async (script) => {
        let element = document.createElement('script');
        element.innerText = script.innerText;
        document.head.appendChild(element);        
    });
}