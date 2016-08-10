var fs = require('fs');
var args = process.argv.slice(2);
var referenceFile = 'package.json';

if (args[0] != null) {
	referenceFile = args[0];
}

var json = JSON.parse(fs.readFileSync('package.json', 'utf8'));

fs.readFile('./boiler/redpack.spec', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  
	data = data.replace(/--name--/g, json.name);
	data = data.replace(/--license--/g, json.license);
	data = data.replace(/--description--/g, json.description);
	data = data.replace(/--version--/g, json.version);
	data = data.replace(/--homepage--/g, json.homepage);

  fs.writeFile( json.name+'.spec', data, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});
