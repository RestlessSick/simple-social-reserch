const copy_url = async (url) => {
    await fetch(url).then(response => {
        if (!response.ok) {
            message('Cant copy to clipboard.');
        }
        else 
            response.text().then(result => {
                navigator.clipboard.writeText(result).then(() => {
                    message('Copied') 
                }).catch(error => message("Unable to copy. Error: " + error));
            });
    });
}