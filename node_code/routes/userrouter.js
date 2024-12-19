const express = require("express");
const router = express.Router();
const conn = require("../config/db");

router.get("/",(req,res)=>{
    res.sendFile(path.join(__dirname, "./build/index.html"));
})

router.post("/", (req, res) => {
    const { user_id, user_pw, user_phone, user_acq_phone, user_addr1, user_addr2, user_keyword } = req.body;
    if (!user_id || !user_pw) {
        return res.status(400).json({ message: "아이디와 비밀번호를 입력하세요." });
    }
    const sql = "INSERT INTO users(user_id, user_pw, user_phone, user_acq_phone, user_addr1, user_addr2, user_keyword) VALUES (?, sha(?), ?, ?, ?, ?, ?)";
    conn.query(sql, [user_id, user_pw, user_phone, user_acq_phone, user_addr1, user_addr2, user_keyword], (err, result) => {
        if (err) {
            console.error("회원가입 실패:", err);
            return res.status(500).json({ message: "회원가입 중 오류가 발생했습니다." });
        }
        res.status(200).json({ result: "success" });
    });
});
  
router.post('/login', (req, res) => {
    let { user_id, user_pw } = req.body;
    if (!user_id || !user_pw){
        return res.status(400).send("<script>alert('아이디와 비밀번호를 입력하세요'); window.location.href = '/login';</script>");
    }
    console.log(req.body)
    let sql = "select * from users where user_id =? and user_pw = sha(?)"
    conn.query(sql, [user_id, user_pw],
        (err, result) => {
            if(err) {
                res.status(500).send("Internal Server Error");
            }
            console.log(result)
            if (result.length > 0) {
                res.status(200).json({result: "success"});
                // res.redirect("/main")
            } else {
                res.status(400).send("Input error");
                // res.send("<script>alert('로그인실패'); window.location.href = '/login</script>")
            }
        })
})

router.get("/image", (req, res) => {
    const { date } = req.query; 
    let sql = "SELECT trg_image FROM triggers";
    const params = [""];
    if (date) { 
        sql += "SELECT trg_image FROM triggers WHERE DATE(trg_at) = ?";
        params.push(date);
    }
    conn.query(sql, params, (err, results) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ error: "이미지 조회 오류" });
        }

        for (let i=0; i< results.length; i++){
            results[i].trg_image = `1218_${i+1}.jpg`
        }
        console.log("쿼리결과:", results)
        res.status(200).json(results);
    });
});

router.get("/video", (req, res) => {
    const { date } = req.query; 
    let sql = "SELECT video_path FROM videos";
    const params = [];
    if (date) { 
        sql += " WHERE DATE(videos) = ?";
        params.push(date);
    }
    conn.query(sql, params, (err, results) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ error: "영상 조회 오류" });       
        }
        console.log("쿼리결과:", results)
        res.status(200).json(results); 
    });
});

router.get("/main", (req, res) => {
    const sql = "SELECT user_acq_phone FROM users WHERE user_id = 'smhrd1'"; 
    conn.query(sql, (err, results) => {
      if (err) {
        console.error("Error fetching contacts:", err);
        return res.status(500).json({ error: "Failed to fetch contacts" });
      }
      res.status(200).json(results); 
    });
  });

router.get("/notifications", (req, res) => {
    const sql = "SELECT trg_info FROM triggers WHERE user_id = 'smhrd1' order by trg_at desc;"; 
    conn.query(sql, (err, results) => {
      if (err) {
        console.error("Error fetching events:", err);
        return res.status(500).json({ error: "Failed to fetch events" });
      }
      res.status(200).json(results); 
    })
  })
 
  router.get("/history", (req,res)=>{
    const sql = "SELECT trg_type, trg_at, trg_info FROM triggers order by trg_at desc"; 
    conn.query(sql, (err, results) => {
        if (err) {
          console.error("Error fetching history:", err);
          return res.status(500).json({ error: "Failed to fetch history" });
        }
        res.status(200).json(results); 
      })
    });
module.exports = router