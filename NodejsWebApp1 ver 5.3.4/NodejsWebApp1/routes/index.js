var express = require('express');
var router = express.Router();

module.exports = function(passport) {

    router.get('/', function(req, res, next) {
        res.render('./Login_v2/index', { message: req.flash('info') });
    })

    router.post('/signin', passport.authenticate('login', {
        successRedirect: '/quiz',
        failureRedirect: '/',
        failureFlash: true
    }));

    function admin_auth(req, res, next) {
        if (req.isAuthenticated() && req.user.username == 'admin') {
            return next()
        }
        res.redirect('/')
    }

    router.get('/admin', admin_auth, function(req, res, next) {
        res.sendFile('admin.html', {
            root: './NodejsWebApp1/views'
        });
    })

    return router;
}