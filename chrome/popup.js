/*
//click handler for the buttons, will prompt you to click on an element to add label
var addLabel = function(type) {
  console.log(type);
};

var element = document.getElementById('price');
element.addEventListener('click', function() { addLabel('price') }, false);

element = document.getElementById('name');
element.addEventListener('click', function() { addLabel('name') }, false);

element = document.getElementById('description');
element.addEventListener('click', function() { addLabel('description') }, false);
*/


//click handler to save page / add to elastic search

window.onload = function() {
  function clickHandler(e) {
    window.location = "http://google.com";
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('button').addEventListener('click', clickHandler);
  });
}

