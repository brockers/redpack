var fs = require('fs');
var args = process.argv.slice(2);
var referenceFile = 'package.json';

var pad = function(n){
	return n<10 ? '0'+n : n;
}

var changelogDate = function(){

	var weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
	var month = ["Jan","Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	var date = new Date();

	var dayOfWeek = weekday[date.getDay()];
	var shortMonth = month[date.getMonth()];
	var dayOfMonth = pad( date.getDate() );

	return dayOfWeek+" "+shortMonth+" "+dayOfMonth+" "+date.getFullYear();
}

if (args[0] != null) {
	referenceFile = args[0];
}

var json = JSON.parse(fs.readFileSync('package.json', 'utf8'));

fs.readFile('./boiler/template-server.spec', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  
	console.log(json.version);
	data = data.replace(/--version--/g, json.version);
	data = data.replace(/--name--/g, json.name);
	data = data.replace(/--license--/g, json.license);
	data = data.replace(/--description--/g, json.description);
	data = data.replace(/--homepage--/g, json.homepage);
	data = data.replace(/--author.name--/g, json.author.name);
	data = data.replace(/--changelog.date--/g, changelogDate());

  fs.writeFile( json.name+'.spec', data, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});
