//========================================================================
// SciKit-SurgeryFRED Introduction
//========================================================================


function startfredo() {

      console.log("starting fred");
      fetch("/startfred", {
      method: "POST",
      headers: {
	"Content-Type": "application/json"
      },
	      body: JSON.stringify({
		      "ok": 0
      	      })
      })
      .then(resp => resp.text())
      .then(data => {
		      console.log(data);
		      document.write(data);
	            })
    .catch(err => {
      console.log("error");
      console.log("An error occured when trying to start fred", err.message);
      window.alert("An error occured when trying to start fred");
    })
}
