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
    console.log(type);
    var requestContext = {
      type: type
    };

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, requestContext, function(){});
    });
  }
};

document.addEventListener('DOMContentLoaded', function () {
  TessLabeler.addEventListeners();
});

// vim: ft=javascript et sw=2 sts=2
