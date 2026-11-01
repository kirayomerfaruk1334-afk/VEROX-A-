from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("POLLINATIONS_API_KEY")

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VEROX AI</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;background:#090e19;color:#f4f7ff;
 font-family:Arial,sans-serif;height:100vh;
 display:flex;overflow:hidden
}
#sidebar{
 width:260px;background:#101827;padding:18px;
 display:flex;flex-direction:column;gap:15px;
 border-right:1px solid #25334a;
}
.logo{font-size:25px;font-weight:bold;color:#36d7ff;letter-spacing:3px}
.new{
 background:#17273a;color:white;border:1px solid #30445e;
 padding:13px;border-radius:12px;text-align:left;
 font-size:15px;cursor:pointer
}
#history{overflow:auto;flex:1}
.old{
 padding:11px;border-radius:9px;color:#b8c6d9;
 overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
 cursor:pointer;font-size:14px
}
.old:hover{background:#1b2b40}
#main{flex:1;display:flex;flex-direction:column;min-width:0}
header{
 height:65px;border-bottom:1px solid #25334a;
 display:flex;align-items:center;padding:0 18px;gap:12px
}
#menu{display:none}
.status{margin-left:auto;color:#42dfa0;font-size:12px}
#chat{
 flex:1;overflow-y:auto;padding:24px 18px;
 width:100%;max-width:850px;margin:auto
}
.welcome{text-align:center;margin:10vh auto 35px}
.orb{
 width:76px;height:76px;border-radius:50%;
 margin:auto auto 20px;
 background:radial-gradient(circle,#48e3ff,#0879b9,#14213b);
 box-shadow:0 0 35px #008fc966;
 display:grid;place-items:center;font-size:35px;font-weight:bold
}
h1{font-size:30px;margin:10px}
.subtitle{color:#9aabc2}
.cards{
 display:grid;grid-template-columns:1fr 1fr;
 gap:12px;max-width:600px;margin:25px auto
}
.card{
 background:#121e30;border:1px solid #293d58;
 padding:17px;border-radius:15px;cursor:pointer
}
.card:hover{border-color:#25cafa}
.card b{display:block;margin-bottom:7px}
.card small{color:#9aabc2}
.msg{
 padding:14px 17px;border-radius:17px;
 margin:14px 0;line-height:1.6;
 white-space:pre-wrap;overflow-wrap:anywhere;
 max-width:90%
}
.user{background:#0878a9;margin-left:auto}
.bot{background:#17243a;border:1px solid #263c57}
#bottom{padding:12px 16px 20px}
.composer{
 max-width:760px;margin:auto;display:flex;gap:9px;
 background:#152238;border:1px solid #354c69;
 padding:9px;border-radius:20px
}
input{
 flex:1;min-width:0;background:transparent;
 border:0;outline:0;color:white;font-size:16px;padding:10px
}
button{cursor:pointer}
.send{
 border:0;background:#24cafa;color:#061321;
 border-radius:13px;padding:0 18px;font-weight:bold
}
.note{text-align:center;color:#75859c;font-size:11px;margin-top:10px}
@media(max-width:650px){
 #sidebar{display:none;position:absolute;z-index:5;height:100%;width:260px}
 #sidebar.open{display:flex}
 #menu{display:block;background:none;color:white;border:0;font-size:23px}
 #chat{padding:15px}
 .welcome{margin-top:9vh}
 h1{font-size:25px}
}
</style>
</head>
<body>
<aside id="sidebar">
 <div class="logo">✦ VEROX</div>
 <button class="new" onclick="newChat()">＋ Yeni sohbet</button>
 <div style="color:#8295ae;font-size:12px">SOHBETLER</div>
 <div id="history"></div>
 <div style="color:#8295ae;font-size:12px">VEROX AI · V1.1</div>
</aside>

<main id="main">
<header>
 <button id="menu" onclick="toggleMenu()">☰</button>
 <b>VEROX AI</b>
 <span class="status">● ONLINE</span>
</header>

<div id="chat">
 <div class="welcome" id="welcome">
  <div class="orb">V</div>
  <h1>VEROX'a hoş geldin.</h1>
  <div class="subtitle">Bugün sana nasıl yardımcı olabilirim?</div>
  <div class="cards">
   <div class="card" onclick="suggest('Bana bir Python kodu yaz')">
    <b>⌘ Kod yaz</b><small>Projelerine yardım et</small>
   </div>
   <div class="card" onclick="suggest('Bana yaratıcı fikirler ver')">
    <b>✧ Fikir üret</b><small>Yeni şeyler keşfet</small>
   </div>
   <div class="card" onclick="suggest('Bana bir konu öğret')">
    <b>▤ Öğren</b><small>Yeni bilgiler edin</small>
   </div>
   <div class="card" onclick="suggest('Beni eğlendir')">
    <b>☼ Eğlen</b><small>Biraz sohbet edelim</small>
   </div>
  </div>
 </div>
</div>

<div id="bottom">
 <div class="composer">
  <input id="question" placeholder="VEROX'a mesaj yaz..." autocomplete="off">
  <button class="send" onclick="send()">➤</button>
 </div>
 <div class="note">VEROX AI bazen hata yapabilir. Önemli bilgileri kontrol et.</div>
</div>
</main>

<script>
let messages=[];
let chats=[];
let current=-1;

function newChat(){
 messages=[];
 current=-1;
 document.getElementById("chat").innerHTML='<div class="welcome" id="welcome"><div class="orb">V</div><h1>VEROX\\'a hoş geldin.</h1><div class="subtitle">Bugün sana nasıl yardımcı olabilirim?</div><div class="cards"><div class="card" onclick="suggest(\\'Bana bir Python kodu yaz\\')"><b>⌘ Kod yaz</b><small>Projelerine yardım et</small></div><div class="card" onclick="suggest(\\'Bana yaratıcı fikirler ver\\')"><b>✧ Fikir üret</b><small>Yeni şeyler keşfet</small></div><div class="card" onclick="suggest(\\'Bana bir konu öğret\\')"><b>▤ Öğren</b><small>Yeni bilgiler edin</small></div><div class="card" onclick="suggest(\\'Beni eğlendir\\')"><b>☼ Eğlen</b><small>Biraz sohbet edelim</small></div></div></div>';
 document.getElementById("question").focus();
}

function toggleMenu(){
 document.getElementById("sidebar").classList.toggle("open");
}
function suggest(text){
 document.getElementById("question").value=text;
 send();
}
function bubble(text,who){
 let d=document.createElement("div");
 d.className="msg "+who;
 d.textContent=text;
 document.getElementById("chat").appendChild(d);
 return d;
}
function renderHistory(){
 let h=document.getElementById("history");
 h.innerHTML="";
 chats.forEach((c,i)=>{
  let d=document.createElement("div");
  d.className="old";
  d.textContent="▸ "+c.title;
  d.onclick=()=>loadChat(i);
  h.appendChild(d);
 });
}
function loadChat(i){
 current=i;
 messages=JSON.parse(JSON.stringify(chats[i].messages));
 document.getElementById("chat").innerHTML="";
 messages.forEach(m=>{
  if(m.role!=="system") bubble(m.content,m.role==="user"?"user":"bot");
 });
 toggleClose();
}
function toggleClose(){
 document.getElementById("sidebar").classList.remove("open");
}
async function send(){
 let input=document.getElementById("question");
 let q=input.value.trim();
 if(!q)return;
 input.value="";
 let welcome=document.getElementById("welcome");
 if(welcome)welcome.remove();
 if(current===-1){
  current=chats.length;
  chats.push({title:q.slice(0,35),messages:[]});
 }
 bubble(q,"user");
 messages.push({role:"user",content:q});
 let loading=bubble("VEROX düşünüyor...","bot");
 let oldMessages=[{role:"system",content:"Sen VEROX AI adında Türkçe konuşan yardımsever bir yapay zekasın."},...messages];
 try{
  let r=await fetch("/chat",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({messages:oldMessages})
  });
  let data=await r.json();
  loading.textContent=data.reply||data.error||"Hata oluştu.";
  if(data.reply)messages.push({role:"assistant",content:data.reply});
  chats[current].messages=JSON.parse(JSON.stringify(messages));
  renderHistory();
 }catch(e){
  loading.textContent="Bağlantı hatası. Tekrar dene.";
  messages.pop();
 }
 document.getElementById("chat").scrollTop=document.getElementById("chat").scrollHeight;
}
document.getElementById("question").addEventListener("keydown",e=>{
 if(e.key==="Enter")send();
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify(error="API anahtarı bulunamadı."), 500
    try:
        r = requests.post(
            "https://gen.pollinations.ai/v1/chat/completions",
            headers={"Authorization": "Bearer " + API_KEY},
            json={
                "model": "openai/gpt-5.4-nano",
                "messages": request.json.get("messages", [])
            },
            timeout=90
        )
        r.raise_for_status()
        answer = r.json()["choices"][0]["message"]["content"]
        return jsonify(reply=answer)
    except Exception:
        return jsonify(error="VEROX şu anda cevap veremiyor."), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
