var redirect = function(url) {
  chrome.tabs.getCurrent(function(tab) {
    chrome.tabs.update(tab.id, { url: url });
  });
};

// vim: ft=javascript et sw=2 sts=2
