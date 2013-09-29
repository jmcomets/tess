var TessClient = {
  baseURL: 'http://192.168.66.33:5000',
  label: function(url, yes_no) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', baseURL + '/api/label', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send('label=' + yes_no + '&url=' + encodeURI(url));
  }
};

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "label") {
    TessClient.label(window.location.href, request.yes_no);
  }
});

// vim: ft=javascript et sw=2 sts=2
