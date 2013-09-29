var redirect = function(url) {
  chrome.tabs.getCurrent(function(tab) {
    chrome.tabs.update(tab.id, { url: url });
  });
};

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.method == "getContext") {
    console.log("Loaded");
    var documentContext = {
      method: "documentContext",
  url : window.location.protocol + window.location.hostname + window.location.pathname,
  title : document.title,
  event: event
    };

    console.log("Sending docContext");
    chrome.extension.sendRequest(documentContext, function(){});
    console.log("docContext sent.");
  }
});

// vim: ft=javascript et sw=2 sts=2
