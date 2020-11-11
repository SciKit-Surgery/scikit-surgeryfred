//========================================================================
// Drag and drop image handling
//========================================================================

var fileDragL = document.getElementById("file-drag-l");
var fileSelectL = document.getElementById("file-upload-l");

// Add event listeners
fileDragL.addEventListener("dragover", fileDragHover, false);
fileDragL.addEventListener("dragleave", fileDragHover, false);
fileDragL.addEventListener("drop", fileSelectHandler, false);
fileSelectL.addEventListener("change", fileSelectHandler, false);

var fileDragR = document.getElementById("file-drag-r");
var fileSelectR = document.getElementById("file-upload-r");

// Add event listeners
fileDragR.addEventListener("dragover", fileDragHover, false);
fileDragR.addEventListener("dragleave", fileDragHover, false);
fileDragR.addEventListener("drop", fileSelectHandler, false);
fileSelectR.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();
  target_id = e.target.id;
  console.log('Target id ' + target_id)
  fileDragL.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
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
var imagePreviewR = document.getElementById("image-preview-r");
var imageDisplay = document.getElementById("image-display");
var uploadCaptionL = document.getElementById("upload-caption-l");
var uploadCaptionR = document.getElementById("upload-caption-r");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");
var imageLeft = 0;
var imageRight = 0;

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  console.log("submit");

  if (!imageLeft || !imageRight) {
    window.alert("Please select images!");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  // call the predict function of the backend
  predictImage(imageLeft, imageRight);
}

function clearImage() {
  // reset selected files
  fileSelectL.value = "";

  // remove image sources and hide them
  imageLeft = 0;
  imageRight = 0;
  imagePreviewL.src = "";
  imagePreviewR.src = "";

  imageDisplay.src = "";
  predResult.innerHTML = "";

  hide(imagePreviewL);
  hide(imagePreviewR);

  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  show(uploadCaptionL);
  show(uploadCaptionR);

  imageDisplay.classList.remove("loading");
}

function previewFile(file, target_id) {
  // show the preview of the image
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    if ((target_id == "file-upload-l") || (target_id == "file-drag-l")) {
      imagePreviewL.src = URL.createObjectURL(file);

      show(imagePreviewL);
      hide(uploadCaptionL);
    } else {
      imagePreviewR.src = URL.createObjectURL(file);

      show(imagePreviewR);
      hide(uploadCaptionR);
    }
    // reset
    predResult.innerHTML = "";
    imageDisplay.classList.remove("loading");

    if ((target_id == "file-upload-l") || (target_id == "file-drag-l")) {
      //displayImage(reader.result, "image-display");
      console.log('Saving left');
      imageLeft = reader.result;
    } else {
      console.log('Saving right');
      imageRight = reader.result;
    }
  }
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image_l, image_r) {
  console.log("predict");

  var left_right = {};
  left_right.left = image_l;
  left_right.right = image_r;

  fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(left_right)
    })
    .then(resp => {
      console.log("resp");
      if (resp.ok)
        resp.json().then(data => {
          console.log("resp2");

          displayResult(data);
        });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  // imageDisplay.classList.remove("loading");
  // hide(loader);
  // predResult.innerHTML = data.result;
  // show(predResult);
  console.log("received");
  //TODO Display properly
  show(imageDisplay);
  let display = document.getElementById("image-display");
  display.src = data.image_url;
  imageDisplay.classList.remove("loading");
  hide(loader);


}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}