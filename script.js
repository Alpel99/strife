socket = io.connect('http://' + document.domain + ':' + location.port + '/game');
let width_orig = 1920
let height_orig = 1080
let width = window.innerWidth
let height = window.innerHeight
let gamestate = null
let update = true
let h_arr = [500, 800]
let l_arr = [0, 550]

// var debugID = window.setInterval(callDebug, 500);

function callDebug() {
  if(gamestate) {
    console.log(gamestate.terrain)
  }
}

function setup() {
  frameRate(30)
  textAlign(CENTER);
}
  
function draw() {
  resizeCanvas(width, height);
  scale(window.innerWidth/width_orig, window.innerHeight/height_orig)
  background(126);
  if(!socket.connected) {
    push();
    textSize(100);
    textAlign(CENTER);
    fill(255,255,0);
    text("DISCONNECTED", width_orig/2, height_orig/3)
    pop();
  }
  if(gamestate) {
    drawTerrain(gamestate.terrain)
    drawPlayers(gamestate.players)
    drawScores(gamestate)
  }
  sendInputs()
}

function drawTerrain(terrain_arr) {
  stroke(0)
  strokeWeight(4)
  for(let i = 1; i < terrain_arr.length/width_orig+1; i++) {
    for(let j = 0; j < width_orig; j++) {
      var low = height_orig-l_arr[i-1]
      var high = height_orig-(terrain_arr[j*i]*h_arr[i-1])
      line(j,low,j,high)
    }
  }
  strokeWeight(0);
  fill(0,128,0);
  // var h = h_arr[0]*0.03 + 25;
  // console.log(height_orig-h)
  rect(0, 1060, width_orig, height_orig);
}

function drawPlayers(players) {
  players.forEach((p, index) => {
    var col = p.side ? color(0,0,255) : color(255,0,0);
    fill(col);
    // console.log(p)
    var size = 50
    switch(p.state) {
      case 1:
        rect(p.pos[0]-25, p.pos[1]-size/2, 50, 50);
        break;
      case 2:
        ellipse(p.pos[0], p.pos[1]+size/2-size/4, size, size/2);
        break;
      case 3:
        var offset = p.facing ? size/2+50 : -(size/2+50);
        triangle(p.pos[0]+offset, p.pos[1], p.pos[0], p.pos[1]-size/2, p.pos[0], p.pos[1]+size/2);
        break;
      case 0:
        ellipse(p.pos[0], p.pos[1], size);
      default:
        ellipse(p.pos[0], p.pos[1], size);
    }
  });
}

function drawScores(gamestate) {
  var t_size_side = 60;
  var t_size_mid = 80;
  textSize(t_size_side);
  fill(255,0,0)
  text(gamestate.left_score.toString(), 100, t_size_side + 5)
  fill(0,0,255)
  text(gamestate.right_score.toString(), width_orig-100, t_size_side + 5);
  var col = gamestate.global_score > 0 ? color(0,0,255) : color(255,0,0);
  var col = gamestate.global_score == 0 ? color(0,0,0) : col;
  textSize(80);
  fill(col);
  text(abs(gamestate.global_score).toString(), width_orig/2 - t_size_mid/2, t_size_mid + 5);
}

function sendInputs() {
  var m = {
    "up": false,
    "right": false,
    "left": false,
    "down": false,
    "space": false,
    "attack": false,
    "dash": false,
  }
  if(keyIsDown(65) || keyIsDown(37)) {
    m.left = true
  }
  if(keyIsDown(87) || keyIsDown(38)) {
    m.up = true
  }
  if(keyIsDown(68) || keyIsDown(39)) {
    m.right = true
  }
  if(keyIsDown(83) || keyIsDown(40)) {
    m.down = true
  }
  if(keyIsDown(32)) {
    m.space = true
  }
  if(keyIsDown(81) || keyIsDown(75)) { // Q and K
    m.attack = true
  }
  if(keyIsDown(76) || keyIsDown(69)) { // L and E
    m.dash = true
  }
  drawKeyPressed("W", 100, height_orig-h_arr[0]*0.5+55, m.up);
  drawKeyPressed("A", 60, height_orig-h_arr[0]*0.5+100, m.left);
  drawKeyPressed("S", 100, height_orig-h_arr[0]*0.5+100, m.down);
  drawKeyPressed("D", 140, height_orig-h_arr[0]*0.5+100, m.right);

  drawKeyPressed("SPACE", width_orig-100, height_orig-h_arr[0]*0.5+50, m.space);
  drawKeyPressed("Q/K", width_orig-100, height_orig-h_arr[0]*0.5+100, m.attack);
  drawKeyPressed("E/L", width_orig-100, height_orig-h_arr[0]*0.5+150, m.dash);

  // var m = JSON.stringify(message);
  socket.emit("input", m);
}

function drawKeyPressed(t, x, y, pressed) {
  push();
  textSize(40);
  fill(255);
  if (pressed) {
    strokeWeight(2);
    stroke(128)
  } else {
    strokeWeight(0);
  }
  text(t, x, y);
  pop();
}

socket.on('game_update', function(data) {
  switch(data.id) {
    case 0:
      gamestate = data;
      break;
    default:
      console.log(data);
  }
  // console.log("Received message: " + m.id);
});