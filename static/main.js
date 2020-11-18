//======================================================================== // Drag and drop image handling
//========================================================================

// Add event listeners


function loadDefaultContour() {
  fetch("/defaultcontour", {
    method: "POST",
    })
    .then(resp => {
      console.log("resp");
      if (resp.ok)
        resp.json().then(data => {
	  console.log("resp OK");
          displayResult(data);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured", err.message);
      window.alert("An error occured when loading default contour.");
    });

}

//========================================================================
// Web page elements for functions to use
//========================================================================

var preOpImage = document.getElementById("pre-operative-image");
var uploadCaptionL = document.getElementById("upload-caption-l");
var loader = document.getElementById("loader");

//Do this at start up
loadDefaultContour();

//========================================================================
// Main button events
//========================================================================

function changeImage() {
  // action for the change image button
  console.log("Change Image not Implemented");

  window.alert("Change image not implemented!");
  return;

  // call the predict function of the backend
}

function reset() {
  console.log("Reset not Implemented");
  // not implemented
}

//========================================================================
// Helper functions
//========================================================================

function contourImage(image_l) {
  console.log("contour");

  fetch("/contour", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(image_l)
    })
    .then(resp => {
      console.log("resp");
      if (resp.ok)
      	resp.json().then(data => {
	  console.log("resp OK");
          displayResult(data);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayResult(data) {
  console.log("received");
  var canvas = document.getElementById("intra-operative-image");
  if (canvas.getContext) {
    var ctx = canvas.getContext('2d');

    ctx.lineStyle = 'rgb(255, 0, 0)';
    ctx.beginPath();
    data.contour.forEach(function (item, index) {
      ctx.lineTo(item[1], item[0]);
    });
    ctx.closePath();
    ctx.stroke();

  }

}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
