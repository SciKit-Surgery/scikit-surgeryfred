//======================================================================== // Drag and drop image handling
//========================================================================

var fileDragL = document.getElementById("file-drag-l");
var fileSelectL = document.getElementById("file-upload-l");

// Add event listeners
fileDragL.addEventListener("dragover", fileDragHover, false);
fileDragL.addEventListener("dragleave", fileDragHover, false);
fileDragL.addEventListener("drop", fileSelectHandler, false);
fileSelectL.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();
  target_id = e.target.id;
  console.log('Target id ' + target_id)
  fileDragL.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

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

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  target_id = e.target.id;
  console.log(target_id);
  for (var i = 0, f;
    (f = files[i]); i++) {
    previewFile(f, target_id);
  }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreviewL = document.getElementById("image-preview-l");
var imageDisplay = document.getElementById("image-display");
var uploadCaptionL = document.getElementById("upload-caption-l");
var loader = document.getElementById("loader");
var imageLeft = 0;

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

function previewFile(file, target_id) {
  // show the preview of the image
  console.log(file);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  console.log("loading");
  reader.onloadend = () => {
    if ((target_id == "file-upload-l") || (target_id == "file-drag-l")) {
      imagePreviewL.src = URL.createObjectURL(file);
      show(imagePreviewL);
      console.log('Saving left');
      imageLeft = reader.result;
    }
    else{console.log("not", target_id);}
  console.log("loaded");

    imageDisplay.classList.remove("loading");
  }
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
