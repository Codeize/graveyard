const WatchdogClient = require('./Structures/WatchdogClient');
const config = require('../config.json');

const client = new WatchdogClient(config);
client.start();
