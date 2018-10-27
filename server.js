var mysql = require('mysql');
var io = require('socket.io');
var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "123456",
  database: "yelp_db"
});

var io = require('socket.io').listen(80); // initiate socket.io server

io.sockets.on('connection', function (socket) {
  

  /*socket.emit('news', { hello: 'world' }); // Send data to client*/

  // wait for the event raised by the client
  socket.on('userData', function (data) {  
    console.log(data.lat+","+data.lon+","+data.radius);
    var lat = data.lat;
	var lon = data.lon;
	var radius = data.radius;
	//var q = 'select * from business where latitude limit 2';
	var q = 'select name, stars, latitude, longitude,( 6371 * acos(cos( radians('+lat+' ) ) *cos( radians(latitude) ) * cos( radians(longitude) - radians( '+lon+' )) + sin(radians('+lat+')) *sin(radians(latitude)))) as distance FROM restaurantz HAVING distance < '+radius+' ORDER BY distance LIMIT 25';
	console.log(q);
	con.query(q, function (err, result, fields) {
	socket.emit('output',{result});
    console.log(result);
  });
  });
});


/*
con.connect(function(err) {
  if (err) throw err;
  con.query("select * from yelp_business limit 1", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});*/