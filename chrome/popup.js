var TessLabeler = {
  yesElement: null,
  noElement: null,
  redirectElement: null,
  labelElement: null,
  init: function() {
    var self = this;
    self.yesElement = document.getElementById('yes');
    self.noElement = document.getElementById('no');
    self.labelElement = document.getElementById('label');
    self.redirectElement = document.getElementById('redirect');
    self.yesElement.addEventListener('click', function() { self.label(true); });
    self.noElement.addEventListener('click', function() { self.label(false); });
    self.labelElement.style.display = 'block';
    self.redirectElement.style.display = 'none';
  }, label: function(yes_no) {
    var self = this;
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        type: 'label', yes_no: yes_no
      });
      self.redirectElement.innerHTML = '';
      self.labelElement.style.display = 'none';
      self.redirectElement.style.display = 'block';
      chrome.tabs.sendMessage(tabs[0].id, {
        type: 'get_link'
      }, function(response) {
        var centerElement = document.createElement('center');
        if (response.url === undefined) {
          setTimeout(function() { window.close(); }, 3000);
          centerElement.innerText = 'No links available...';
        } else {
          var urlElement = document.createElement('a');
          urlElement.href = response.url;
          urlElement.innerText = 'Next page ?';
          urlElement.addEventListener('click', function() {
            chrome.tabs.sendMessage(tabs[0].id, { type: 'redirect', url: response.url });
            window.close();
          });
          centerElement.appendChild(urlElement);
        }
        self.redirectElement.appendChild(centerElement);
      });
    });
  }
};

document.addEventListener('DOMContentLoaded', function () { TessLabeler.init(); });

// vim: ft=javascript et sw=2 sts=2
