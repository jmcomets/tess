var TessClient = {
  baseURL: 'http://0.0.0.0:5000',
  label: function(url, yes_no) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', this.baseURL + '/api/label', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send('label=' + yes_no + '&url=' + encodeURI(url));
  }
};

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type == 'label') {
    TessClient.label(window.location.href, request.yes_no);
  } else if (request.type == 'get_link') {
    var aTags = document.getElementsByTagName('a'),
      a = aTags[Math.floor(Math.random()*aTags.length)],
      data = {}
    if (a !== undefined) { data['url'] =  a.href }
    sendResponse(data);
  } else if (request.type == 'redirect') {
    window.location.href = request.url;
  }
});

// vim: ft=javascript et sw=2 sts=2
