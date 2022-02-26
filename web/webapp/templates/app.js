// apparently this is re-implementing some of React
var render = function (template, node) {
  node.innerHTML = template;
}


mybutton = "<button type='button' class='button' onclick='pokeESP32(event);'>Buzz</button>";

function submitPW() {
  event.preventDefault();
  var submittedPassword = document.getElementById("password").value;
  if (submittedPassword == "password") {
    render(mybutton, document.querySelector("div#testing"));
  } else {
    render("Wrong", document.querySelector("div#testing"));
  }
}



var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.send( null );
    }
}

function pokeESP32() {
  alert("Buzzing");
  var client = new HttpClient();
  var target = "http://192.168.1.145/printIp";
  client.get(target, function(response) {
    // do something with response
  });
}
