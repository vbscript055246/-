const mongoose = require('mongoose');
var Schema = mongoose.Schema;

var NormReferenced = new Schema({
    quiz_class: Number,
    quiz_no: Number,
    value: String
});

module.exports = mongoose.model('NmRef',NormReferenced);