'use strict';

var express = require('express');
var app = express();

app.get('/webhook', function (req, res) {
    res.send('Hello Totos');
})
