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
      window.alert("Oops! Something went wrong.");
    });

}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreviewL = document.getElementById("image-preview-l");
var imageDisplay = document.getElementById("image-display");
var uploadCaptionL = document.getElementById("upload-caption-l");
var loader = document.getElementById("loader");
var imageLeft = 0;

//Do this at start up
loadDefaultContour();

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  console.log("submit", imageLeft);

  if (!imageLeft) {
    window.alert("Please select image!");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  // call the predict function of the backend
  console.log(imageLeft);
  contourImage(imageLeft);
}

function clearImage() {
  // reset selected files
  fileSelectL.value = "";

  // remove image sources and hide them
  imageLeft = 0;
  imagePreviewL.src = "";

  imageDisplay.src = "";

  hide(imagePreviewL);
	
  drawBlank();
  hide(loader);
  show(uploadCaptionL);

  imageDisplay.classList.remove("loading");
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
  var canvas = document.getElementById("image-display");
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
