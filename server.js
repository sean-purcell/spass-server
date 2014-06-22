var http = require('http'),
      fs = require('fs');

var server = http.createServer(handler);

server.listen(8000);

var page = fs.readFileSync('main.html');

function handler(req, res) {
	console.log(req.method + ":" + req.url);
	if(req.method == 'GET') {
		res.writeHead(200, {'Content-Type': 'text/html'});
		res.write(page);
		res.end();
	} else if(req.method == 'POST') {
		req.on('data', function(chunk) {
			console.log('data:' + chunk);
		});
	}
}
