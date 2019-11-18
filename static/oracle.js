function fetch_oracle(o) {
    fetch(typeof o === 'undefined' ? '/oracles/api/v1' : '/oracles/api/v1/' + o)
        .then((resp) => resp.json())
        .then(function(data) {
            document.getElementById('oracle').innerHTML = data.oracle;
            path = data.path.replace('/api/v1', '');
            window.location = data.api_uri.replace('/api/v1', '');
            output = data.text + ' (<a href=\'' + path + '\'>link</a>, <a href=\'' + data.api_uri + '\'>API</a>)'; 
            document.getElementById('text').innerHTML = output;
        })
        .catch(function() {console.log('did not get it');});
}
