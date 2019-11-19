function fetch_oracle(o) {
  fetch(typeof o === 'undefined' ? '/oracles/api/v1' : '/oracles/api/v1/' + o)
    .then((resp) => resp.json())
    .then(function(data) {
      document.getElementById('oracle').innerHTML = data.oracle;
      window.location = window.location.origin + data.path;
      document.getElementById('text').innerHTML = `${data.text} \
        (<a href='${data.path}'>link</a>, \
        <a href='${data.api_uri}'>API</a>)`;
    })
    .catch(function() {console.log('did not get it');});
}
