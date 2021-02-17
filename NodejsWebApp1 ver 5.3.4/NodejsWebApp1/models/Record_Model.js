const mongoose = require('mongoose');
var Schema = mongoose.Schema;

var UserMsgSchema = new Schema({
    username: String, // user ID
    mode: Number, // cooperation or solo
    quiz_class: Number, // what kinds of quizziz
    quiz_no: Number, // acctural quiz No.
    quiz_ans: String, // user Ans
    Msgdate: Date // the time msg send
});

module.exports = mongoose.model('UserMsg', UserMsgSchema);