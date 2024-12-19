const mysql = require("mysql2");

const conn = mysql.createConnection({
    host : "project-db-cgi.smhrd.com",
    port : 3307,
    user : "campus_24IS_IOT2_p2_1",
    password : "smhrd1",
    database : "campus_24IS_IOT2_p2_1"
})

conn.connect((err)=>{
    if (err) {
        console.error("MySQL 연결 실패:", err);
      } else {
        console.log("MySQL 연결 성공!");
      }
});

module.exports = conn;
