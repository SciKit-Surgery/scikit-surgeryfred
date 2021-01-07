//========================================================================
// SciKit-SurgeryFRED game logic
//========================================================================

var dial; 
const scores = [];
var repeats = 0;

YUI().use('dial', function(Y) {

        dial = new Y.Dial({
        min:0,
        max:20,
	decimalPlaces:1,
        stepsPerRevolution:2,
        value: 1,
	strings : {
		label: 'Margin',
		resetStr:'Reset',
		tooltipHandle:'Drag to ablation margin'
	}
        });
        dial.render('#ablation_dial');


        });


function enable_ablation() {
	document.getElementById("ablation_button").disabled = false;
	document.getElementById("ablation_button").style.backgroundColor = "#de1712";
};

function disable_ablation() {
	document.getElementById("ablation_button").disabled = true;
	document.getElementById("ablation_button").style.backgroundColor = "#f0f0f0";
};

function ablate() {
	var margin = dial.get('value');
	console.log("Ablating: ", margin);
	console.log("Target: ", target); //target from main.js
	console.log("Transformed Target: ", transformed_target); //trans target from main.js
	console.log(calculatescore(margin));
	//get target pos.
};

function calculatescore(margin) {
	fetch("/calculatescore", {
		method: "POST",
		headers: {
        	    "Content-Type": "application/json"
      		},
		body: JSON.stringify({
			"target": target,
			"est_target": transformed_target,
			"target_radius": target_radius,
			"margin": margin
		})
	})
	.then(resp => {
		resp.json().then(data => {
			console.log(data.score);
		});
	})
	.catch(err => {
            console.log("An error occured calculating the score.", err.message);
      });
};
