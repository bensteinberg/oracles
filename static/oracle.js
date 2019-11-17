function fetch_oracle() {
    fetch('/api/v1')
        .then((resp) => resp.json())
        .then(function(data) {
            document.getElementById('oracle').innerHTML = data.oracle;
            path = data.path.replace('/api/v1', '');
            window.location = data.api_uri.replace('/api/v1', '');
            output = data.text + ' (<a href=\'' + path + '\'>permalink</a>, <a href=\'' + data.api_uri + '\'>API</a>)'; 
            document.getElementById('text').innerHTML = output;
        })
        .catch(function() {console.log('did not get it');});
}
