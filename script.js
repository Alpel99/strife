let ws = new WebSocket("ws://localhost:8000");
let width_orig = 1920
let height_orig = 1080
let width = window.innerWidth
let height = window.innerHeight
let gamestate = null
let update = true

function setup() {
  frameRate(60)
  resizeCanvas(width, height);
}
  
function draw() {
  scale(window.innerWidth/width_orig, window.innerHeight/height_orig)
  background(126);
  if(gamestate) {
    drawTerrain(gamestate.terrain)
    drawPlayers(gamestate.players)
    drawScores(gamestate)
  }
sendInputs()
}

function drawTerrain(terrain_arr) {
  h_arr = [500, 800]
  l_arr = [0, 550]
  stroke(0)
  strokeWeight(4)
  for(let i = 1; i < terrain_arr.length/width_orig+1; i++) {
    for(let j = 0; j < width_orig; j++) {
      line(j,height_orig-l_arr[i-1],j,height_orig-(terrain_arr[j*i]*h_arr[i-1]))
    }
  }
  strokeWeight(0)
}

function drawPlayers(players) {
  players.forEach((p, index) => {
    console.log(p.position)
    ellipse(p.position[0], height_orig-p.position[1], 50)
  });
}

function drawScores(gamestate) {
  textSize(40);
  fill(255,0,0)
  text(gamestate.left_score.toString(), 100, 50)
  fill(0,0,255)
  text(gamestate.right_score.toString(), width_orig-100, 50)
  fill(0,0,255)
  textSize(55);
  text(gamestate.global_score.toString(), width_orig/2 - 50, 50)
}

function sendInputs() {
  var message = {
    "id": 1,
    "up": 0,
    "right": 0,
    "left": 0,
    "down": 0,
    "space": 0
  }

  if(keyIsDown(65) || keyIsDown(37)) {
    message.left = 1
  }
  if(keyIsDown(87) || keyIsDown(38)) {
    message.up = 1
  }
  if(keyIsDown(68) || keyIsDown(39)) {
    message.right = 1
  }
  if(keyIsDown(83) || keyIsDown(40)) {
    message.down = 1
  }
  if(keyIsDown(32)) {
    message.space = 1
  }
  var m = JSON.stringify(message);
  ws.send(m);
}

ws.onopen = function() {
  var message = { 
    "id": -1
  }
  var m = JSON.stringify(message);
  ws.send(m);
};

ws.onmessage = function(event) {
  var message = event.data
  var m = JSON.parse(message)
  console.log(m.players[0].position);
  switch(m.id) {
    case 0:
      gamestate = m;
    default:
      console.log(m);
  }
  // console.log("Received message: " + m.id);
};