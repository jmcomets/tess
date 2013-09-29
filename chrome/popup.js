var TessLabeler = {
  addEventListeners: function() {
    var self = this;
    document.getElementById('yes').addEventListener('click', function(e) {
      self.label("yes");
    });
    document.getElementById('no').addEventListener('click', function(e) {
      self.label("no");
    });
  },
  label: function(type) {
    var requestContext = {
      method: "getContext",
      event: event
    }
    chrome.tabs.sendMessage(tabId, requestContext, function(){}); 
  }
};

document.addEventListener('DOMContentLoaded', function () {
  TessLabeler.addEventListeners();
});

// vim: ft=javascript et sw=2 sts=2
