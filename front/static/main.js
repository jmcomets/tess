$(function() {
  var QUERY_URL = "/api/search?query=",
    AC_URL = "/api/auto_suggest",
    $resultBox = $('.result-box'),
    $searchBar = $('#search-bar'),
    options = {
      serviceUrl: AC_URL,
      onSelect: function(value, data) {
        renderResults(value.value);
      }
    };

$searchBar.autocomplete(options);

$searchBar.keyup(function(e) {
  e.stopPropagation();
  e.preventDefault();

  var text = $searchBar.val();
  renderResults(text);
});

function renderResults(text) {
  if (!text) return;

  var query_url = QUERY_URL + formatForUrl(text);
  $.getJSON(query_url, function(data) {
    var html = new EJS({ url: '/static/results.ejs' }).render(data);
    $resultBox.html(html);
    history.pushState('', '', '/' + formatForUrl(text));
  });
}

function formatForUrl(str) {
  var separator = ' ';
  return encodeURI(str.replace(/_/g, separator)
    .replace(/ /g, separator)
    .replace(/:/g, separator)
    .replace(/\\/g, separator)
    .replace(/\//g, separator)
    //.replace(/[^a-zA-Z0-9\-]+/g, '')
    .replace(/-{2,}/g, separator)
    .toLowerCase());
};

// if push state
var pathName = document.location.pathname;
if (pathName !== '/') {
  if (pathName.substring(0,1) === '/') {
    pathName = pathName.substring(1, pathName.length);
  }
  if (pathName.substring(pathName.length - 1, pathName.length) === '/') {
    pathName = pathName.substring(0, pathName.length - 1);
  }

  $.getJSON(QUERY_URL + formatForUrl(pathName), function(data) {
    //console.log(data);
    var html = new EJS({ url: '/static/results.ejs' }).render(data);
    $resultBox.html(html);
  });
}
});

// vim: ft=javascript et sw=2 sts=2
