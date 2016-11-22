var connect = require('connect');
var fs = require('fs');

try {
  fs.mkdirSync(__dirname + '/raw-data');
}
catch(ex) {}
if (!fs.existsSync(__dirname + '/classification')) {
  fs.writeFileSync(__dirname + '/classification', '', 'utf-8');
}

connect()
    .use(connect.static(__dirname))
    .listen(9321, '0.0.0.0');

fs.watch('./classification', function(curr, prev) {
  if (!curr) return;
  fs.readFile('./classification', 'utf-8', function(err, data) {
    if (err) {
      return console.error('Cannot read classification file', err);
    }
    console.log('Classification is now', data);
    broadcast(JSON.stringify({
      type: 'classification',
      classification: data.match(/\d/g)
    }));
  });
});




var logged = {};
var firstwrite = {};
var iteration = 0;

var ws = require("nodejs-websocket");
var server = ws.createServer(function(conn) {

  var to;
  conn.on("text", function(str) {

    if (to) {
      clearTimeout(to);
    }

    var data;
    try {
      data = JSON.parse(str);

      if (data.deviceId) {
        conn.deviceId = data.deviceId;
      }
    }
    catch (ex) {}

    if(data.type=='pingClient'){
      sendDevice(JSON.stringify({type:'adminPing'}), data.deviceId)
    }

    if(data.type=='status'){
      console.log(data.status);
    }
    /*if(conn.deviceId=='Admin'){
      console.log("New connection", conn.deviceId);
      return false;
    }*/

    if(data.type=='createFile'){
      iteration = data.iteration;
      console.log("Creating new file", conn.deviceId);
      fs.appendFileSync(__dirname + '/raw-data/' + conn.deviceId + iteration,
        'sep=;\ntimestamp;gyro-alpha;gyro-beta;gyro-gamma;accel-x;accel-y;accel-z\n',
        'utf-8');
      firstwrite[conn.deviceId] = true;
    }

    if (conn.deviceId && !logged[conn.deviceId]) {
      console.log("New connection", conn.deviceId);
      logged[conn.deviceId] = true;
      sendAdmin(JSON.stringify({type:'newConnection', deviceId: conn.deviceId}));
    }

    // no message for 2s, then treat as disconnect
    if (conn.deviceId) {
      to = setTimeout(function() {
        broadcast(JSON.stringify({ type: 'client-gone', deviceId: conn.deviceId }));
      }, 2000);
    }

    broadcast(str);

    if (!data.gyro || !data.accel) return;

    var cs = [
      data.timestamp,
      data.gyro.alpha,
      data.gyro.beta,
      data.gyro.gamma,
      data.accel.x,
      data.accel.y,
      data.accel.z
    ].join(';');

    if (!firstwrite[conn.deviceId]) {
      //var DID = conn.deviceId;
      console.log("Start measurement", conn.deviceId);
      fs.appendFileSync(__dirname + '/raw-data/' + conn.deviceId + iteration,
        'sep=;\ntimestamp;gyro-alpha;gyro-beta;gyro-gamma;accel-x;accel-y;accel-z\n',
        'utf-8');
      firstwrite[conn.deviceId] = true;
    }

    fs.appendFile(__dirname + '/raw-data/' + conn.deviceId + iteration,
      cs + '\n',
      'utf-8',
      function(err) {
        if (err) {
          console.error('Writing data', conn.deviceId, 'failed', err);
        }
      });
  });
  conn.on("close", function(code, reason) {
    broadcast(JSON.stringify({ type: 'client-gone', deviceId: conn.deviceId }));
    sendAdmin(JSON.stringify({type:'closedConnection', deviceId: conn.deviceId}));
    console.log("Connection closed", conn.deviceId);
  });
}).listen(9322, '0.0.0.0');

function broadcast(msg) {
  server.connections.forEach(function(conn) {
    if(conn.deviceId!='Admin'){
      try {
        conn.sendText(msg);
      }
      catch(ex) {}
    }
  });
}

function sendAdmin(msg){
  server.connections.forEach(function(conn) {
    if(conn.deviceId=='Admin'){
      try {
        conn.sendText(msg);
      }
      catch(ex) {}
    }
  });
}

function sendDevice(msg, deviceId){
  server.connections.forEach(function(conn) {
    if(conn.deviceId==deviceId){
      try {
        conn.sendText(msg);
      }
      catch(ex) {}
    }
  });
}

process.on('uncaughtException', function (err) {
  console.error(err.stack);
});

console.log('Listening on port', 9321);
