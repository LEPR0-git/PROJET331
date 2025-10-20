
let express = require("express");

let app = express();

app.get("/",(request,response)=>{
        response.send("Bienvenue sur notre backend ");	
})
