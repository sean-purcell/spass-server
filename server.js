var http = require('http'),
      fs = require('fs'),
    querystring = require('querystring'),
    exec = require('child_process').exec;

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
		var fullbody = '';
		req.on('data', function(chunk) {
			//console.log('data:' + chunk);
			fullbody += chunk;
		});
		req.on('end', function() {
			var data = querystring.parse(fullbody);
			console.log(data.pwname);
			exec('echo "' + data.mpw + '\n" | spass get ' + data.pwname,
				function(err, stdout, stderr) {
					if(err) {
						res.writeHead(500);
						res.end();
						return;
					}
					res.writeHead(200, {'Content-Type': 'text/plain'});
					res.write(stdout);
					res.write(stderr);
					res.end();
				}
			);
		});
	}
}
