var TessLabeler = {
  addEventListeners: function() {
    document.getElementById('yes').addEventListener('click', function(e) {
      alert("here");
    });
  }
};

document.addEventListener('DOMContentLoaded', function () {
  TessLabeler.addEventListeners();
});
