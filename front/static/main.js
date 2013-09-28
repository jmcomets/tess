var QUERY_URL = "/api/search?query=",
    $resultBox = $('.result-box');

$('#search-btn').click(function(e) {
  e.stopPropagation();
  e.preventDefault();

  var text = $('#search-bar').val();
  if (!text) return;

  $.getJSON(QUERY_URL + formatForUrl(text), function(data) {
    //console.log(data);
    var html = new EJS({ url: '/static/results.ejs' }).render(data);
    $resultBox.html(html);
    history.pushState("", "", formatForUrl(text));
  });
});

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

//if push state
$.getJSON(QUERY_URL + formatForUrl(text), function(data) {
    //console.log(data);
    var html = new EJS({ url: '/static/results.ejs' }).render(data);
    $resultBox.html(html);
  });
// vim: ft=javascript et sw=2 sts=2
