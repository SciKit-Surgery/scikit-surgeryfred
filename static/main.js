//========================================================================
// SciKit-SurgeryFRED front end
//========================================================================

// Add event listeners
preOpImage = document.getElementById("pre-operative-image");
intraOpImage = document.getElementById("intra-operative-image");

preOpImage.addEventListener("click", preOpImageClick)
intraOpImage.addEventListener("click", intraOpImageClick)


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

var uploadCaptionL = document.getElementById("upload-caption-l");
var loader = document.getElementById("loader");

//Do this at start up
loadDefaultContour();

//========================================================================
// Main button events
//========================================================================

function preOpImageClick(evt) {
	console.log("PreOp Image Clicked", evt);
}

function intraOpImageClick(evt) {
	console.log("IntraOp Image Clicked", evt);
}

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
  var canvas = intraOpImage; 
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
