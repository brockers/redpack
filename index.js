var fs = require('fs')

fs.readFile('./boiler/redpack.spec', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  var result = data.replace(/--name--/g, 'replacement');

  fs.writeFile('someFile.spec', result, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});
