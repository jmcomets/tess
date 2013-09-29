var TessLabeler = {
  addEventListeners: function() {
    var self = this;
    document.getElementById('yes').addEventListener('click', function(e) {
      self.label(true);
    });
    document.getElementById('no').addEventListener('click', function(e) {
      self.label(false);
    });
  }, label: function(yes_no) {
    var requestContext = {
      type: "label",
      yes_no: yes_no
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
