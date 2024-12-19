const express = require("express");
const app = express();
const bp = require("body-parser");
const nunjucks = require("nunjucks");
const morgan = require("morgan");
const cors = require("cors");
const path = require('path');
const userrouter = require("./routes/userrouter");
const conn = require("./config/db");
const multer = require('multer');
const fs = require('fs');

app.use(express.json());
app.use(cors());
app.use(morgan("combined"));
app.use(bp.json());
app.use(bp.urlencoded({extended : true}))
app.use(express.static(path.join(__dirname, "build",'index.html')));
app.use("/", userrouter);
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use('/videos', express.static(path.join(__dirname, 'videos')));

app.listen(3001);