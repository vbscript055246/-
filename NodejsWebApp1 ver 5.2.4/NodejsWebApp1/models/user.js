var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var UserSchema = new Schema({
    username: String, //user ID
    password: String, //user password
    logindate: Date //last login time
});

module.exports = mongoose.model('User', UserSchema);