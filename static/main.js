//========================================================================
// SciKit-SurgeryFRED front end
//========================================================================

//global variables

//store the contour for the intra-opimage
var intraOpContour = [[200,100], [300,100], [300,400], [200, 400] ];
var canvasScale = 4; //scale the canvases so we can zoom in
var dbreference = 0; //reference to the database document

//lists of fiducial markers and target
const preOpFids = [];   //moving
const intraOpFids = []; //fixed
var target = [];

//the fiducial localisation errors
var preOpFLEStdDev = [];
var intraOpFLEStdDev = [];
var preOpFLEEAV = 0;
var intraOpFLEEAV = 0;

//page elements for convenience
var preOpImage = document.getElementById("pre-operative-image");
var preOpCanvas = document.getElementById("pre-operative-canvas");
var intraOpContourCanvas = document.getElementById("intra-operative-contour");
var intraOpFiducialCanvas = document.getElementById("intra-operative-fiducials");
var intraOpTargetCanvas = document.getElementById("intra-operative-target");

// Add event listeners

preOpCanvas.addEventListener("click", preOpImageClick)
intraOpTargetCanvas.addEventListener("click", intraOpImageClick)


async function loadDefaultContour() {
  console.log("Default contour");
  fetch("/defaultcontour", {
    method: "POST",
    })
    .then(resp => {
      console.log("resp");
      if (resp.ok)
        resp.json().then(data => {
          intraOpContour = data.contour;
          drawOutline(intraOpContour);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured", err.message);
      window.alert("An error occured when loading default contour.");
    });
    return 1;
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var uploadCaptionL = document.getElementById("upload-caption-l");
var loader = document.getElementById("loader");

//Do this at start up
startup();

//========================================================================
// Main button events
//========================================================================

async function startup() {
    const result = await loadDefaultContour();	
    console.log(result);
    resetTarget();
    init_fles();
    initdatabase();
}

function preOpImageClick(evt) {
	console.log("PreOp Image Clicked", evt);
	placeFiducial(evt.layerX, evt.layerY);
}

function intraOpImageClick(evt) {
	console.log("IntraOp Image Clicked", evt);
	placeFiducial(evt.layerX, evt.layerY);
}

function changeImage() {
  // action for the change image button
  console.log("Change Image not Implemented");

  window.alert("Change image not implemented!");
  return;
}

function reset(){
  console.log('reset');
  resetTarget();
  clearCanvas(intraOpTargetCanvas);
  clearCanvas(intraOpFiducialCanvas);
  init_fles();

  preOpFids.length = 0;
  intraOpFids.length = 0;
}

function placeFiducial(x, y) {
      fetch("/placefiducial", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify([x, y, preOpFLEStdDev, intraOpFLEStdDev])
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
	  if ( data.valid_fid ) {
          var intraOpFid = data.fixed_fid;
          var preOpFid = data.moving_fid;
	  drawMeasuredFiducial(preOpFid, preOpCanvas);
	  drawActualFiducial([x,y], preOpCanvas);
	  drawMeasuredFiducial(intraOpFid, intraOpFiducialCanvas);
	  drawActualFiducial([x,y], intraOpFiducialCanvas);

	  preOpFids.push(preOpFid);
	  intraOpFids.push(intraOpFid);
	  register();
          console.log(preOpFids);
          console.log(intraOpFids);
	  };
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured fetching new target", err.message);
      window.alert("An error occured fetching new target");
    });
}
 
function register(){
      fetch("/register", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify([target, preOpFLEEAV, intraOpFLEEAV, preOpFids, intraOpFids])
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
		if ( data.success ){
		  console.log(data.fre);
		  console.log(data.actual_tre);
		  clearCanvas(intraOpTargetCanvas);
          	  drawTarget(data.transformed_target, intraOpTargetCanvas);
          	  drawActualTarget(target, intraOpTargetCanvas);
		  writeresults(data.fre, data.actual_tre);
		};
	});
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured during registration", err.message);
      window.alert("An error occured during registration");
    });

}

function writeresults(fre, tre){
  console.log("Writing results to ", dbreference)
  fetch("/writeresults", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify([dbreference, fre, tre])

    })
    .catch(err => {
      console.log("error");

      console.log("An error occured during write", err.message);
      window.alert("An error occured during registration");
    });
}

function initdatabase(){
  fetch("/initdatabase", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
		console.log("Get write ref:", data, data.reference);
		dbreference = data.reference;
		console.log(dbreference);
	});
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured during write", err.message);
      window.alert("An error occured during registration");
    });
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
          intraOpContour = data.contour;
          drawOutline(intraOpContour);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function resetTarget() {
  console.log("reset target called");
  fetch("/gettarget", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify(intraOpContour)
    })
    .then(resp => {
      console.log("New Target");
      if (resp.ok)
        resp.json().then(data => {
          target = [data.target[0][1], data.target[0][0], 0.0]
	  clearCanvas(preOpCanvas);
          drawTarget(target, preOpCanvas);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured fetching new target", err.message);
      window.alert("An error occured fetching new target");
    });

}

function init_fles() {
  fetch("/getfle", {
      method: "POST",
    })
    .then(resp => {
      console.log("Setting fle");
      if (resp.ok)
        resp.json().then(data => {

	preOpFLEStdDev = data.moving_fle_sd;
        intraOpFLEStdDev = data.fixed_fle_sd;
        preOpFLEEAV = data.moving_fle_eav;
        intraOpFLEEAV = data.fixed_fle_eav;
	console.log(data);
      });
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured fetching new target", err.message);
      window.alert("An error occured fetching new target");
    });

}

//========================================================================
// Drawing Functions
//========================================================================
function drawOutline(contour) {
  console.log("received");
  var canvas = intraOpContourCanvas; 
  if (canvas.getContext) {
    var ctx = canvas.getContext('2d');

    ctx.strokeStyle = "#808080";
    ctx.lineWidth = 3 * canvasScale;
    ctx.beginPath();
    contour.forEach(function (item, index) {
      ctx.lineTo(item[1] * canvasScale, item[0] * canvasScale);
    });
    ctx.closePath();
    ctx.stroke();
  }
 
}

function clearCanvas(canvas) {
  if (canvas.getContext) {
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

function drawTarget(local_target, canvas) {
  if (canvas.getContext) {
	  console.log(local_target);
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = "#880000";
    ctx.beginPath();
    ctx.arc(local_target[0] * canvasScale , local_target[1] * canvasScale, 5 * canvasScale, 0, 2 * Math.PI);
    ctx.fill();
  }
}

function drawCross(position, canvas, strokeStyle, linewidth, length){
  if (canvas.getContext) {
    var ctx = canvas.getContext('2d');
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = linewidth;
    ctx.beginPath();
    ctx.moveTo(position[0] * canvasScale - length * canvasScale, position[1] * canvasScale)
    ctx.lineTo(position[0] * canvasScale + length * canvasScale, position[1] * canvasScale)
    ctx.moveTo(position[0] * canvasScale, position[1] * canvasScale - length * canvasScale)
    ctx.lineTo(position[0] * canvasScale, position[1] * canvasScale + length * canvasScale)
    ctx.stroke();
  }
}

function drawActualFiducial(position, canvas){
	drawCross(position, canvas, "#000000", 1, 3)
}
function drawActualTarget(position, canvas){
	drawCross(position, canvas, "#0000FF", 2, 5)
}

function drawMeasuredFiducial(position, canvas){
 if (canvas.getContext) {
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = "#ff0000";
    ctx.beginPath();
    ctx.arc(position[0] * canvasScale, position[1] * canvasScale, 3 * canvasScale, 0, 2 * Math.PI);
    ctx.fill();
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
