var QUERY_URL = "/search?query=",
    $resultBox = $('.result-box');

$('#search-btn').click(function(e) {
  e.stopPropagation();
  e.preventDefault();

  var text = $('#search-bar').val();
  if (!text) return;

  $.getJSON(QUERY_URL + formatForUrl(text), function(data) {
    console.log(data);
    var html = new EJS({url: '/static/results.ejs'}).render(data);
    $resultBox.html(html);
  });
});

function formatForUrl(str) {
  return str.replace(/_/g, '-')
    .replace(/ /g, '-')
    .replace(/:/g, '-')
    .replace(/\\/g, '-')
    .replace(/\//g, '-')
    .replace(/[^a-zA-Z0-9\-]+/g, '')
    .replace(/-{2,}/g, '-')
    .toLowerCase();
};
