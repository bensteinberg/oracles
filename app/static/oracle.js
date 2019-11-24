function fetch_oracle(o) {
  fetch(typeof o === 'undefined' ? '/oracles/api/v1' : '/oracles/api/v1/' + o)
    .then((resp) => resp.json())
    .then(function(data) {
      document.getElementById('oracle').innerHTML = data.oracle;
      window.history.pushState({}, "Oracles", window.location.origin + data.path);
      document.getElementById('text').style.display = "block";
      document.getElementById('text').innerHTML = `${data.text} \
        (<a href='${data.path}'>link</a>, \
        <a href='${data.api_uri}'>API</a>)`;
      document.getElementById('reversal').style.display = "none";
      document.getElementById('reversal').innerHTML = `${data.reversal} (<em>flipped</em>)`;
      document.getElementById('flip').innerHTML = 'flip';
    })
    .catch(function() {console.log('did not get it');});
}

function flip() {
  flipped = document.getElementById('reversal').style.display == "block";
  document.getElementById('text').style.display = flipped ? "block" : "none";
  document.getElementById('reversal').style.display =flipped ? "none" : "block";
  document.getElementById('flip').innerHTML = flipped ? "flip" : "back";
}
