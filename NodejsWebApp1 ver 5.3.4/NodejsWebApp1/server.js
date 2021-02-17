port = 8888;


const express = require('express');
const path = require('path');
const app = express();

const server = require('http').Server(app);
const io = require('socket.io')(server);

const colors = require('colors');

colors.setTheme({
    silly: 'rainbow',
    input: 'grey',
    verbose: 'cyan',
    prompt: 'grey',
    info: 'green',
    data: 'grey',
    help: 'cyan',
    warn: 'yellow',
    debug: 'blue',
    error: 'red'
});

// DB connect
var mongoose = require('mongoose');
var config = require('./db');
mongoose.connect(config.connection);
mongoose.connection.on('connected', function() {
    console.log('Mongoose connection succeed~');
});

// DB models
var UserMsg = require('./models/Record_Model.js');
// var User = require('./models/user.js');

// passport setting
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy
var session = require('express-session');

//"擴散指導語1", "擴散指導語2", "遠距聯想指導語1", "遠距聯想指導語2"
var mode_list = [
    [11, 14, 22, 25, 13, 16], //甲
    [15, 12, 24, 21, 16, 13], //乙
    [25, 22, 14, 11, 16, 13], //丙
    [21, 24, 12, 15, 13, 16], //丁
    [11, 14, 22, 25], //戊
    [15, 12, 24, 21], //己
    [25, 22, 14, 11], //庚
    [21, 24, 12, 15]  //辛    
];

var mode_ptr = -1;
var stage_ptr = -1;
var admin_next_switch = 0;
var socket_array = [];

var indexRouter = require('./routes/index')(passport);

//=======================================
var Mutex = require('async-mutex').Mutex;
const mutex = new Mutex();
var onlineUserArray = [];



function startTimer(duration) {
    var time = duration;
    var x = setInterval(function() {
        io.emit("update_time", time);
        if (--time < 0) {
            clearInterval(x);
            admin_next_switch = 0; // second close switch
            stage_ptr++;
            io.to("admin").emit("user_ready"); // to admin 
            // io.emit("update_time", 0);
        }
    }, 1000);
}

function record(msg) {

    for (var i = 0; i < msg["data"].length; i++) {
        var No = msg["data"][i]["quizNo"];
        var Ans = msg["data"][i]["quizData"];
        var Ans_data = new UserMsg({
            username: msg["userid"],
            mode: parseInt(msg["mode"] / 10),
            quiz_class: msg["mode"] % 10,
            quiz_no: No,
            quiz_ans: Ans,
            Msgdate: msg["data"][i]["time"]
        });

        Ans_data.save(function(err, data) {
            if (err) {
                console.error("Error:" + err);
            } else {
                //console.info("Rec:" + data);
            }
        });
    }
}

// passport

passport.serializeUser(function(user, done) {
    done(null, user.username);
})

passport.deserializeUser(function(id, done) {
    var user = { username: id, password: id };
    return done(null, user);
});

passport.use('login', new LocalStrategy({
        usernameField: 'username',
        passwordField: 'password',
        passReqToCallback: true
    },
    function(req, username, password, done) {
        if (username[0] == 'S' || username[0] == 's') {
            username = parseInt(username.replace('S', 0).replace('s', 0));
        }
        var user = { username: username, password: username };
        if (username != 'admin') {
            if (parseInt(username) % 10000 == parseInt(password)) {
                return done(null, user);
            }
        } else {
            if (password == 'admin') {
                return done(null, user);
            }
        }

        return done(null, false, req.flash('info', 'Incorrect password or account.'));
    }
));

// setting link to app
var flash = require('connect-flash');
var cookieParser = require('cookie-parser');

var sessionMiddleware = session({
    secret: '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225',
    resave: false,
    saveUninitialized: false
});

io.use(function(socket, next) {
    sessionMiddleware(socket.request, socket.request.res, next);
});

app.use(sessionMiddleware);

app.use(passport.initialize())
app.use(passport.session())
app.use(flash());

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

//app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// routing
app.use('/', indexRouter);

function authenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next()
    }
    res.redirect('/')
}

// User .slice(1)
function setCookie(req, res) {
    res.cookie('userid', parseInt(req.user.username), { path: '/' });
    res.cookie('mode', mode_list[mode_ptr][stage_ptr], { path: '/' });
}

app.get('/quiz', authenticated, function(req, res, next) {
    if (req.user.username == 'admin') {
        res.cookie('userid', req.user.username, { path: '/admin' });
        res.redirect('/admin');
    } else {
        socket_array.push(parseInt(req.user.username));
        next = setCookie(req, res);
        res.sendFile('base.html', {
            root: './NodejsWebApp1/views'
        });
    }
})


app.use(express.static(path.join(__dirname, 'views/Login_v2')));

// catch 404 and forward to error handler
var createError = require('http-errors');
app.use(function(req, res, next) {
    next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});


// Socket
io.on('connection', (socket) => {
    var userOnlieName = "";

    // admin set mode
    socket.on("SetQuizMode", (data) => {
        console.log("admin set signal");
        mode_ptr = data;
        stage_ptr = 0;
    });

    // next quiz
    socket.on("admin_next", function() {
        io.to('admin').emit("return_stage_ptr", stage_ptr);
        //console.log(mode_list[mode_ptr].length);
        if (stage_ptr < mode_list[mode_ptr].length) {
            // to everyone
            io.emit("next");
        } else {
            io.emit("end");
        }
    });

    //start quiz
    socket.on("admin_startquiz", function() {
        admin_next_switch = 1;

        // load quiz
        io.emit("startquiz");

        // start timer
		startTimer(5);

    });

    // update online# to admin
    socket.on("setChannel", (arg) => {
        console.log("Channel set request");
        socket.join(arg);
        userOnlieName = arg;
		//console.log(arg);
		if (arg == "admin") return;
		//console.log("acquire key");
		mutex.acquire().then(function(release){
			//console.log("get key");
			onlineUserArray.push(parseInt(arg));
			io.to("admin").emit("online_user", onlineUserArray);
            io.to("admin").emit("online", onlineUserArray.length);
			//console.log("add event");
			//console.log(onlineUserArray);
			release();
			//console.log("key back");
		});
    });

    // update online# to admin when lose connect
    socket.on('disconnect', () => {
		
		mutex.acquire().then(function(release){
			//console.log("dis");
			//console.log(userOnlieName);
			
			var ind = onlineUserArray.indexOf(parseInt(userOnlieName));
			if (ind != -1) onlineUserArray.splice(ind, 1);
			//console.log("remove event");
			//console.log(onlineUserArray);
			io.to("admin").emit("online_user", onlineUserArray);
			io.to("admin").emit("online", onlineUserArray.length); //to admin
			release();
		});
    });

    // partner msg send
    socket.on("send_ans", (msg) => {
        //console.log("from " + msg['sender']);
        msg['sender'] % 2 ? msg['sender']-- : msg['sender']++;
        //console.log("send to " + msg['sender']);
        io.to(msg['sender']).emit("mateText", msg);
    });

    socket.on("get_switch_state", (arg) => {
        io.to(arg).emit("return_switch_state", admin_next_switch);
    });

    socket.on("save_ansQueue", (arg) => {
        socket.request.session.ansQueue = arg;
    });

    socket.on("restore_ansQueue", (arg) => {
        io.to(arg).emit("return_ansQueue", socket.request.session.ansQueue);
    });

    //write ans to DB
    socket.on("submit", (msg) => {
        record(msg);
    });
});

// =====================================
server.listen(port, () => {
    console.log((`+---------------------------------------+\n` +
        `|  Server Started http://localhost:` + port + ` |\n` +
        `+---------------------------------------+\n`).rainbow);
});