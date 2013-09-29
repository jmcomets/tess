chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "yes") {
    console.log("yes");
    //save link and 1
  } else {
    console.log("no");
    //save link and 0
  }
});


// vim: ft=javascript et sw=2 sts=2
