//========================================================================
// SciKit-SurgeryFRED game logic
//========================================================================

var dial; 
const scores = [];
var repeats = 0;
var total_score = 0;

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
	calculatescore(margin);
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
			scores.push(data.score);
			total_score = total_score + data.score;
			repeats = repeats - 1;
			updateGameStats();
			if ( repeats == 0 )
				endgame();
			else
				reset();

		});
	})
	.catch(err => {
            console.log("An error occured calculating the score.", err.message);
      });
};

function gameMode() {
        console.log("pressed game button", state, repeats)
	if ( state == "game" ) //are already in game mode ?
	{
		if ( repeats == 0 ) //we can go back to FRED
		{
			hideGameElements();
			switchToFred();
			button = document.getElementById('game_button');
    			button.value="Play Game"
			show(document.getElementById('plot_button'));
			show(document.getElementById('newtargetbutton'));
			show(document.getElementById('downloadbutton'));
		}
	}
	else
	{
		if ( state == "plot" ) {
			switchToFred();
		}

		console.log("Entering Game Mode");
		scores.length = 0;
		repeats = 20;
		total_score = 0;
		showGameElements();
		updateGameStats();
	        button = document.getElementById('game_button');
    		button.value="Back to Fred";
		hide(button);
		hide(document.getElementById('plot_button'));
		hide(document.getElementById('newtargetbutton'));
		hide(document.getElementById('downloadbutton'));
		reset();
		state = "game";
	}

};

function endgame() {
	show(document.getElementById('game_button'));
};


	
function updateGameStats() {
	document.getElementById('repeats').innerHTML = repeats;
	document.getElementById('totalscore').innerHTML = total_score;
	if (scores.length > 0) 
		document.getElementById('lastscore').innerHTML = scores[scores.length - 1];
	else
		document.getElementById('lastscore').innerHTML = 0;
};


function showGameElements(){
        document.querySelectorAll('.scorebox').forEach(function(el) {
        show(el);
        });
        document.querySelectorAll('.gameelement').forEach(function(el) {
        show(el);
        });

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


};
