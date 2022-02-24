function submitPW() {
  event.preventDefault();
  var submittedPassword = document.getElementById("password").value;
  if (submittedPassword == "password") {
    window.location.href="right.html";
  } else {
    window.location.href="wrong.html";
  }
}

function pokeESP32() {
  IP = XXXXX;
  websocket.send("open");
}
