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
    if(p.blocking) {
      rect(p.pos[0]-25, p.pos[1]-25, 50, 50);
    } else if(p.attacking) {
      var offset = p.side ? -50 : 50
      triangle(p.pos[0]+offset, p.pos[1], p.pos[0], p.pos[1]-25, p.pos[0], p.pos[1]+25)
    } else {
      ellipse(p.pos[0], p.pos[1], 50);
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
  var message = {
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
  // var m = JSON.stringify(message);
  socket.emit("input", message);
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