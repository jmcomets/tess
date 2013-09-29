var TessLabeler = {
  addEventListeners: function() {
    var self = this;
    document.getElementById('yes').addEventListener('click', function(e) { self.label(true); });
    document.getElementById('no').addEventListener('click', function(e) { self.label(false); });
  }, label: function(yes_no) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        type: 'label', yes_no: yes_no
      }, function() {});
      document.getElementById('label').style.display = 'none';
      document.getElementById('redirect').style.display = 'block';
      var aTags = document.getElementsByTagName('a'),
        url = aTags[Math.floor(Math.random()*aTags.length)];
    });
  }
};

document.addEventListener('DOMContentLoaded', function () {
  TessLabeler.addEventListeners();
  document.getElementById('label').style.display = 'block';
  document.getElementById('redirect').style.display = 'none';
});

// vim: ft=javascript et sw=2 sts=2
