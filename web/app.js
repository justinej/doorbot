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

function pokeESP32() {
  alert("Buzzing");
  // IP = XXXXX;
  // websocket.send("open");
}
