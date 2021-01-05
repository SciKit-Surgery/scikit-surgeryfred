//========================================================================
// SciKit-SurgeryFRED front end
//========================================================================

//global variables
var state = "fred" // fred, plot or game

//store the contour for the intra-opimage
var intraOpContour = [[200,100], [300,100], [300,400], [200, 400] ];
var canvasScale = 4; //scale the canvases so we can zoom in
var dbreference = 0; //reference to the database document

//arrays of the results, decided to store these locally, to 
//avoid problems when we're not connected to a data base, and 
//to avoid many read calls.
const results = [];

//lists of fiducial markers and target
const preOpFids = [];   //moving
const intraOpFids = []; //fixed
var target = [];

//the fiducial localisation errors
var FLE;

//page elements for convenience
var preOpImage = document.getElementById("pre-operative-image");
var preOpCanvas = document.getElementById("pre-operative-canvas");
var intraOpContourCanvas = document.getElementById("intra-operative-contour");
var intraOpFiducialCanvas = document.getElementById("intra-operative-fiducials");
var intraOpTargetCanvas = document.getElementById("intra-operative-target");

const actualTREText = document.getElementById("actual-TRE");
const actualFREText = document.getElementById("actual-FRE");
const expectedTREText = document.getElementById("expected-TRE");
const expectedFREText = document.getElementById("expected-FRE");
const expectedFLEText = document.getElementById("expected-FLE");
const noFidsText = document.getElementById("no-fids");

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
	placeFiducial(evt.layerX, evt.layerY);
}

function intraOpImageClick(evt) {
	placeFiducial(evt.layerX, evt.layerY);
}

function downloadResults() {
  let csvContent = "# actual tre, actual fre, expected tre, expected fre, mean fle, number of fids\n";

  results.forEach(function(rowArray) {
    let row = rowArray.join(",");
    csvContent += row + "\r\n";
  });

  download(csvContent, "results.csv", "text/csv");

}

function toScatterData(x_data, y_data){
	//parses array data so it can be used in a chart.js scatter plot
	var data = [];
	
	x_data.forEach(function (item, index){
		data.push({ x: item, y: y_data[index]});
	});
	return data;
}


async function plotResults() {
   if ( state == "fred" ) {
   var correlations = {
	  'corr_coeffs' : [0,0,0,0,0],
	  'xs' : [[0,0],[0,0],[0,0],[0,0],[0,0]],
	  'ys' : [[0,0],[0,0],[0,0],[0,0],[0,0]]
  	};
  
   switchToChartView();
   if ( results.length > 3 ){
     await fetch("/correlation", {
        method: "POST",
        headers: {
        	"Content-Type": "application/json"
        },
        body: JSON.stringify(results)
     })
    .then(resp => {
        if (resp.ok)
          resp.json().then(data => {
		console.log("coreel Data = ", data);
		correlations = data;
    		var treVsFreCanvas = document.getElementById('trevsfre-canvas');
    		makeScatterPlot(1, 'FRE', correlations, treVsFreCanvas);

    		var treVsETreCanvas = document.getElementById('trevsexptre-canvas');
    		makeScatterPlot(2, 'Expected TRE', correlations, treVsETreCanvas);

    		var treVsEFreCanvas = document.getElementById('trevsexpfre-canvas');
    		makeScatterPlot(3, 'Expected FRE', correlations, treVsEFreCanvas);

    		var treVsEFleCanvas = document.getElementById('trevsfle-canvas');
    		makeScatterPlot(4, 'Expected FLE', correlations, treVsEFleCanvas);

    		var treVsNFidsCanvas = document.getElementById('trevsnofids-canvas');
    		makeScatterPlot(5, 'Number of Fiducials', correlations, treVsNFidsCanvas);
	  });
     })
    .catch(err => {
      console.log("An error occured during get correlations", err.message);
    });
    } else {
      console.log("Insufficient results to get correlations, try doing more registrations.");
      window.alert("4 or more regsitration results needed to plot. You have " + results.length + ".");
    }
   }
	else {
		if ( state == "plot" ) {
			switchToFred()
		}
	}

}

function makeScatterPlot(index, xlabel, corrdata, canvas){
	
      scatterData = toScatterData(
	    results.map(function(value, colindex){return value[index];}),
	    results.map(function(value, colindex){return value[0];}));
     
      lineofbestfit = toScatterData(corrdata.xs[index-1], corrdata.ys[index-1])
      const mytitle = new String("TRE vs " + xlabel + " (Corr. Coeff = " +  Math.round(corrdata.corr_coeffs[index - 1]*1000)/1000 + ")");
      var data = {
      datasets: [
        {
            data: scatterData,
	    showLine: false,
            pointBackgroundColor: 'rgba(0,0,0,1.0)'
        },
	{
	    data: lineofbestfit,
	    showLine: true,
	    pointRadius: 0.0,
	    fill: false

	}
      ]
      };

      var ctx = canvas.getContext('2d');
      var xticksconf = {}
      if (index == 2) {
	      xticksconf = {max:20.0};
      }
      var myChart = new Chart(ctx, { type: 'scatter', data , 
      options: { responsive:true,
	      legend: {
		      display: false
	      },
	     title:{text: mytitle ,
		     display: true},
	      scales:{ 
                 yAxes: [{
			 scaleLabel:{
		    		labelString: "Actual TRE",
	            		display: true
			 },
                    ticks: {
                    beginAtZero: true,
		    min: 0.0,
		    max: 20.0
                    }
                 }],
	         xAxes: [{
			 scaleLabel:{
		          labelString: xlabel,
	                  display: true
			 },
			  type: 'linear',
                	  position: 'bottom',
			 ticks: xticksconf
		 }],
             }
        }
      });
}

function switchToFred(){
    console.log("Switching to fred");
    show(preOpImage);
    show(preOpCanvas);
    show(intraOpContourCanvas);
    show(intraOpFiducialCanvas);
    show(intraOpTargetCanvas);
    show(document.getElementById("logo"));
    document.querySelectorAll('.resultbox').forEach(function(el) {
   	show(el);
	});

    hide(document.getElementById('plot-table'));
    button = document.getElementById('plot_button');
    button.value="Plot Results";
    show(document.getElementById('newtargetbutton'));
    state = "fred";
}


function switchToChartView(){
    hide(preOpImage);
    hide(preOpCanvas);
    hide(intraOpContourCanvas);
    hide(intraOpFiducialCanvas);
    hide(intraOpTargetCanvas);
    hide(document.getElementById("logo"));
    document.querySelectorAll('.resultbox').forEach(function(el) {
   	hide(el);
	});
    show(document.getElementById('plot-table'));
    button = document.getElementById('plot_button');
    button.value="Back to Fred";
    hide(document.getElementById('newtargetbutton'));
    state = "plot";
    document.getElementById('result-text').innerHTML = "After " + results.length + " registrations.";
}

function reset(){
  console.log('reset');
  resetTarget();
  clearCanvas(intraOpTargetCanvas);
  clearCanvas(intraOpFiducialCanvas);
  init_fles();
  console.log("FLE = ", FLE);

  preOpFids.length = 0;
  intraOpFids.length = 0;
}

function placeFiducial(x, y) {
      fetch("/placefiducial", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
	      body: JSON.stringify({
		      "x_pos": x,
		      "y_pos": y,
		      "pre_op_ind_fle": FLE.preOpFLEStdDev, 
		      "intra_op_ind_fle": FLE.intraOpFLEStdDev,
		      "pre_op_sys_fle": FLE.preOpSysError, 
		      "intra_op_sys_fle": FLE.intraOpSysError})
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
      body: JSON.stringify([target, FLE.preOpFLEEAV, FLE.intraOpFLEEAV, preOpFids, intraOpFids])
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
		if ( data.success ){
		  results.push([data.actual_tre, data.fre, data.expected_tre, data.expected_fre, data.mean_fle, data.no_fids]);
		  clearCanvas(intraOpTargetCanvas);
          	  drawTarget(data.transformed_target, intraOpTargetCanvas);
          	  drawActualTarget(target, intraOpTargetCanvas);
		  writeresults(data.actual_tre, data.fre, data.expected_tre, data.expected_fre, data.mean_fle, data.no_fids);
		  actualTREText.innerHTML=Math.round(data.actual_tre*100)/100;
		  actualFREText.innerHTML=Math.round(data.fre*100)/100;
		  expectedTREText.innerHTML=Math.round(data.expected_tre*100)/100;
		  expectedFREText.innerHTML=Math.round(data.expected_fre*100)/100;
		  expectedFLEText.innerHTML=Math.round(data.mean_fle*100)/100;
		  noFidsText.innerHTML=data.no_fids;
		};
	});
    })
    .catch(err => {
      console.log("error");

      console.log("An error occured during registration", err.message);
      window.alert("An error occured during registration");
    });

}

function writeresults(actual_tre, fre, expected_tre, expected_fre, mean_fle, no_fids){
  console.log("Writing results to ", dbreference)
  fetch("/writeresults", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify([dbreference, actual_tre, fre, expected_tre, expected_fre, mean_fle, no_fids])

    })
    .catch(err => {
      console.log("An error occured during write", err.message);
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

function resetTarget() {
  console.log("reset target called");
  fetch("/gettarget", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
      body: JSON.stringify({"outline" : intraOpContour})
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

/**
 * Sets the global fiducial localisation error (FLE)
 */
function init_fles() {
  fetch("/getfle", {
      method: "POST",
    })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
	
	let preOpFLEStdDev = data.moving_fle_sd;
        let intraOpFLEStdDev = data.fixed_fle_sd;
        let preOpFLEEAV = data.moving_fle_eav;
        let intraOpFLEEAV = data.fixed_fle_eav;

        let preOpSysError = [0.0, 0.0, 0.0];
        let intraOpSysError = [0.0, 0.0, 0.0];
	
	FLE = { preOpFLEStdDev, intraOpFLEStdDev, 
		preOpFLEEAV, intraOpFLEEAV,
		preOpSysError, intraOpSysError };

      });
    })
    .catch(err => {
      console.log("An error occured setting fles", err.message);
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

