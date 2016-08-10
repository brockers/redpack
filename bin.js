fs = require('fs');
json = JSON.parse(fs.readFileSync('package.json', 'utf8'));
version = json.version;
