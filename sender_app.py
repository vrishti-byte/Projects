import base64
import time
import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from crypto.aes_encryption import generate_aes_key, encrypt_data
from crypto.rsa_encryption import encrypt_key

st.set_page_config(page_title="CRYPTEX // SENDER", layout="wide", initial_sidebar_state="collapsed")

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
*,*::before,*::after{box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stToolbar"]{visibility:hidden!important;}
.block-container{padding:1.5rem 2rem!important;max-width:1400px!important;}
:root{
  --neon:#00ffe7;--neon2:#ff003c;--neon3:#ffe600;
  --bg:#000508;--panel:rgba(0,18,16,0.88);
  --border:rgba(0,255,231,0.2);--text:#9efff5;
  --mono:'Share Tech Mono',monospace;--hud:'Orbitron',monospace;--vt:'VT323',monospace;
}
.stApp{background:var(--bg)!important;}
#bgCanvas{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;}
.scanlines{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.15) 3px,rgba(0,0,0,0.15) 4px);animation:scanMove 12s linear infinite;}
@keyframes scanMove{0%{background-position:0 0;}100%{background-position:0 400px;}}
.vignette{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1;pointer-events:none;background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.8) 100%);}
.stApp>*{position:relative;z-index:2;}
.cyber-header{text-align:center;padding:1rem 0 0.6rem;position:relative;}
.cyber-header::after{content:'';position:absolute;bottom:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,var(--neon),transparent);box-shadow:0 0 14px var(--neon);}
.cyber-title{font-family:var(--hud);font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;color:var(--neon);letter-spacing:6px;text-shadow:0 0 20px var(--neon),0 0 60px rgba(0,255,231,0.35);animation:titlePulse 3s ease-in-out infinite;}
@keyframes titlePulse{0%,100%{text-shadow:0 0 20px var(--neon),0 0 60px rgba(0,255,231,0.35);}50%{text-shadow:0 0 35px var(--neon),0 0 90px rgba(0,255,231,0.55);}}
.cyber-sub{font-family:var(--vt);font-size:1.25rem;color:rgba(0,255,231,0.5);letter-spacing:4px;margin-top:0.4rem;animation:subtleBlink 1.8s step-end infinite;}
@keyframes subtleBlink{0%,100%{opacity:1;}50%{opacity:0.35;}}
.status-bar{display:flex;gap:1.5rem;flex-wrap:wrap;align-items:center;padding:0.5rem 1rem;margin:0.8rem 0;background:rgba(0,15,14,0.7);border:1px solid var(--border);border-radius:3px;font-family:var(--mono);font-size:0.75rem;color:rgba(0,255,231,0.5);}
.s-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--neon);box-shadow:0 0 8px var(--neon);margin-right:6px;animation:dotBlink 1.4s ease-in-out infinite;}
@keyframes dotBlink{0%,100%{opacity:1;}50%{opacity:0.2;}}
.step-card{background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:0.9rem 1.3rem;margin:0.8rem 0;position:relative;overflow:hidden;animation:cardIn 0.45s cubic-bezier(0.23,1,0.32,1) both;transition:border-color 0.3s,box-shadow 0.3s;}
.step-card:hover{border-color:var(--neon);box-shadow:0 0 22px rgba(0,255,231,0.15);}
.step-card.yellow{border-color:rgba(255,230,0,0.4)!important;background:rgba(18,15,0,0.92)!important;}
.step-card.yellow .step-label{color:var(--neon3)!important;}
.step-card.yellow .step-num{border-color:var(--neon3)!important;color:var(--neon3)!important;}
.step-card.yellow::after{border-color:rgba(255,230,0,0.5)!important;}
@keyframes cardIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
.step-card::before{content:'';position:absolute;top:0;left:-120%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(0,255,231,0.06),transparent);animation:shimmer 3s ease-in-out infinite;}
@keyframes shimmer{0%{left:-120%;}100%{left:220%;}}
.step-card::after{content:'';position:absolute;top:5px;right:5px;width:14px;height:14px;border-top:2px solid rgba(0,255,231,0.4);border-right:2px solid rgba(0,255,231,0.4);}
.step-label{font-family:var(--hud);font-size:0.68rem;font-weight:700;color:var(--neon);letter-spacing:3px;text-transform:uppercase;display:flex;align-items:center;gap:0.7rem;margin-bottom:0.15rem;}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border:1.5px solid var(--neon);border-radius:2px;font-size:0.65rem;color:var(--neon);animation:numGlow 2.5s ease-in-out infinite;}
@keyframes numGlow{0%,100%{box-shadow:0 0 6px rgba(0,255,231,0.3);}50%{box-shadow:0 0 14px rgba(0,255,231,0.7);}}
.step-card .bl{position:absolute;bottom:5px;left:5px;width:12px;height:12px;border-bottom:2px solid rgba(0,255,231,0.3);border-left:2px solid rgba(0,255,231,0.3);}
code,pre,[data-testid="stCode"] pre{font-family:var(--mono)!important;font-size:0.8rem!important;background:rgba(0,255,231,0.04)!important;border:1px solid rgba(0,255,231,0.12)!important;border-radius:3px!important;color:#00ffd0!important;line-height:1.65!important;animation:codeIn 0.35s ease both;}
@keyframes codeIn{from{opacity:0;transform:translateX(-6px);}to{opacity:1;transform:translateX(0);}}
.stButton>button{font-family:var(--hud)!important;font-size:0.82rem!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;color:#000!important;background:var(--neon)!important;border:none!important;border-radius:2px!important;padding:0.6rem 2rem!important;box-shadow:0 0 18px rgba(0,255,231,0.6),0 3px 0 rgba(0,150,135,0.9)!important;transition:all 0.15s ease!important;position:relative!important;overflow:hidden!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 32px rgba(0,255,231,0.9),0 5px 0 rgba(0,150,135,0.9)!important;}
.stButton>button:active{transform:translateY(1px)!important;}
textarea{background:rgba(0,12,11,0.9)!important;border:1px solid rgba(0,255,231,0.22)!important;border-radius:3px!important;color:#9efff5!important;font-family:var(--mono)!important;font-size:0.8rem!important;transition:border-color 0.3s,box-shadow 0.3s!important;}
textarea:focus{border-color:var(--neon)!important;box-shadow:0 0 16px rgba(0,255,231,0.25)!important;}
label{font-family:var(--hud)!important;color:var(--neon)!important;font-size:0.72rem!important;letter-spacing:2px!important;}
[data-testid="stFileUploader"]{background:rgba(0,12,11,0.75)!important;border:1px dashed rgba(0,255,231,0.3)!important;border-radius:4px!important;padding:1rem!important;animation:uploaderPulse 3s ease-in-out infinite;}
@keyframes uploaderPulse{0%,100%{border-color:rgba(0,255,231,0.3);box-shadow:none;}50%{border-color:rgba(0,255,231,0.6);box-shadow:0 0 18px rgba(0,255,231,0.12);}}
[data-testid="stFileUploader"] *{font-family:var(--mono)!important;color:var(--text)!important;}
.stProgress>div{background:rgba(0,255,231,0.08)!important;border-radius:2px!important;height:6px!important;border:1px solid rgba(0,255,231,0.12)!important;}
.stProgress>div>div{background:linear-gradient(90deg,var(--neon),#00b8ff)!important;box-shadow:0 0 12px var(--neon)!important;border-radius:2px!important;transition:width 0.7s cubic-bezier(0.4,0,0.2,1)!important;}
[data-testid="stAlert"]{background:rgba(0,255,231,0.05)!important;border:1px solid var(--neon)!important;border-radius:3px!important;box-shadow:0 0 20px rgba(0,255,231,0.12)!important;}
[data-testid="stAlert"] *{color:var(--neon)!important;font-family:var(--mono)!important;}
hr{border-color:rgba(0,255,231,0.12)!important;}
p,span,[data-testid="stMarkdownContainer"] *{font-family:var(--mono)!important;color:var(--text)!important;}
h1{font-family:var(--hud)!important;color:var(--neon)!important;text-shadow:0 0 18px var(--neon)!important;letter-spacing:4px;}
h2,h3{font-family:var(--hud)!important;color:var(--neon)!important;letter-spacing:2px;font-size:0.95rem!important;}
</style>
<div class="scanlines"></div>
<div class="vignette"></div>
<canvas id="bgCanvas"></canvas>
<script>
(function(){
  const c=document.getElementById('bgCanvas');if(!c)return;
  const x=c.getContext('2d');
  function sz(){c.width=window.innerWidth;c.height=window.innerHeight;}
  sz();window.addEventListener('resize',sz);
  const FS=13,CH='01アイウエオABCDEF0123456789{}[]#@$%^&*<>/\\';
  let cols,drops;
  function initD(){cols=Math.floor(c.width/FS);drops=Array.from({length:cols},()=>Math.random()*-(c.height/FS));}
  initD();window.addEventListener('resize',initD);
  const nodes=Array.from({length:50},()=>({x:Math.random()*c.width,y:Math.random()*c.height,vx:(Math.random()-.5)*.45,vy:(Math.random()-.5)*.45,r:Math.random()*1.8+.8,ph:Math.random()*Math.PI*2}));
  const PX=44;
  function draw(){
    x.fillStyle='rgba(0,5,8,0.86)';x.fillRect(0,0,c.width,c.height);
    x.strokeStyle='rgba(0,255,231,0.03)';x.lineWidth=.5;
    for(let i=0;i<c.width;i+=PX){x.beginPath();x.moveTo(i,0);x.lineTo(i,c.height);x.stroke();}
    for(let i=0;i<c.height;i+=PX){x.beginPath();x.moveTo(0,i);x.lineTo(c.width,i);x.stroke();}
    x.fillStyle='rgba(0,255,231,0.08)';
    for(let i=0;i<c.width;i+=PX)for(let j=0;j<c.height;j+=PX)x.fillRect(i-1,j-1,2,2);
    x.font=FS+'px "Share Tech Mono",monospace';
    for(let i=0;i<cols;i++){
      const ch=CH[Math.floor(Math.random()*CH.length)],yy=drops[i]*FS;
      x.fillStyle='rgba(220,255,250,0.85)';x.fillText(ch,i*FS,yy);
      x.fillStyle='rgba(0,255,200,0.14)';x.fillText(CH[Math.floor(Math.random()*CH.length)],i*FS,yy-FS*2);
      x.fillStyle='rgba(0,200,160,0.07)';x.fillText(CH[Math.floor(Math.random()*CH.length)],i*FS,yy-FS*5);
      drops[i]++;if(drops[i]*FS>c.height&&Math.random()>.975)drops[i]=0;
    }
    nodes.forEach((p,i)=>{
      p.x+=p.vx;p.y+=p.vy;p.ph+=0.025;
      if(p.x<0||p.x>c.width)p.vx*=-1;if(p.y<0||p.y>c.height)p.vy*=-1;
      const g=.5+.5*Math.sin(p.ph);
      nodes.forEach((q,j)=>{if(j<=i)return;const d=Math.hypot(p.x-q.x,p.y-q.y);if(d<120){x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.strokeStyle=`rgba(0,255,200,${(1-d/120)*.18*g})`;x.lineWidth=.7;x.stroke();}});
      x.beginPath();x.arc(p.x,p.y,p.r*(0.7+0.5*g),0,Math.PI*2);x.fillStyle=`rgba(0,255,200,${0.45+0.55*g})`;x.shadowBlur=10;x.shadowColor='#00ffe7';x.fill();x.shadowBlur=0;
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cyber-header">
  <div class="cyber-title">⬡ CRYPTEX // SENDER</div>
  <div class="cyber-sub">[ ENCRYPTION TERMINAL ]</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">
  <span><span class="s-dot"></span>SENDER NODE ONLINE</span>
  <span>NODE: COMPUTER A</span>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-card yellow">
  <div class="step-label"><span class="step-num">ℹ</span>HOW THIS WORKS — READ FIRST</div>
  <div class="bl"></div>
  <p style="color:rgba(255,230,0,0.8);font-size:0.82rem;margin-top:0.5rem;line-height:1.8;">
    STEP A → Receiver generates their RSA key pair on Computer B and sends you their PUBLIC KEY<br>
    STEP B → You paste their public key below, then upload your file<br>
    STEP C → This terminal encrypts the file with AES, then locks the AES key using THEIR public key<br>
    STEP D → You send the receiver: Encrypted File Data + Encrypted AES Key<br>
    STEP E → Only the receiver can decrypt because only they have the matching private key
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP A — PASTE RECEIVER'S PUBLIC KEY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label"><span class="step-num">A</span>PASTE RECEIVER'S PUBLIC KEY</div>
  <div class="bl"></div>
</div>
""", unsafe_allow_html=True)

receiver_pubkey_input = st.text_area(
    "RECEIVER'S RSA PUBLIC KEY",
    height=180,
    placeholder="Paste the public key you received from Computer B (Receiver)...\n-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP B — UPLOAD FILE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label"><span class="step-num">B</span>UPLOAD FILE TO ENCRYPT</div>
  <div class="bl"></div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["txt","pdf","png","jpg","docx"], label_visibility="collapsed")

# ── ENCRYPT ONLY WHEN BOTH ARE READY ────────────────────────────────────────
if receiver_pubkey_input.strip() and uploaded_file:

    data = uploaded_file.read()

    st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">01</span>PLAINTEXT DATA — FILE LOADED</div><div class="bl"></div></div>""", unsafe_allow_html=True)
    st.code(data[:300])

    progress = st.progress(0)
    time.sleep(0.3)

    # AES key + encrypt file
    aes_key = generate_aes_key()
    st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">02</span>AES-256 SESSION KEY — GENERATED</div><div class="bl"></div></div>""", unsafe_allow_html=True)
    st.code(aes_key.decode())
    progress.progress(25)
    time.sleep(0.25)

    encrypted_data = encrypt_data(data, aes_key)
    encoded_data   = base64.b64encode(encrypted_data).decode()
    st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">03</span>AES ENCRYPTION — FILE LOCKED</div><div class="bl"></div></div>""", unsafe_allow_html=True)
    st.code(encoded_data[:300])
    progress.progress(55)
    time.sleep(0.25)

    # Load receiver's public key and encrypt the AES key with it
    try:
        pub_key_obj = serialization.load_pem_public_key(receiver_pubkey_input.strip().encode())
        encrypted_key = encrypt_key(aes_key, pub_key_obj)
        encoded_key   = base64.b64encode(encrypted_key).decode()

        st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">04</span>AES KEY — LOCKED WITH RECEIVER'S PUBLIC KEY</div><div class="bl"></div></div>""", unsafe_allow_html=True)
        st.code(encoded_key)
        progress.progress(100)

        st.success("▶  ENCRYPTION COMPLETE — SEND THESE TWO VALUES TO THE RECEIVER")
        st.markdown("---")

        st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">TX</span>SEND THESE TO RECEIVER — NOTHING ELSE NEEDED</div><div class="bl"></div></div>""", unsafe_allow_html=True)

        st.markdown('<p>① ENCRYPTED FILE DATA — paste this into Receiver terminal</p>', unsafe_allow_html=True)
        st.code(encoded_data)

        st.markdown('<p>② ENCRYPTED AES KEY — paste this into Receiver terminal</p>', unsafe_allow_html=True)
        st.code(encoded_key)

        st.info("ℹ  Notice: You do NOT need to send any key. The private key stays with the receiver. This is why RSA is secure.")

    except Exception as e:
        st.error("⚠  INVALID PUBLIC KEY — Make sure you pasted the receiver's full public key correctly")
        st.code(str(e))

elif uploaded_file and not receiver_pubkey_input.strip():
    st.warning("⚠  Paste the receiver's public key first before the encryption can begin.")
elif receiver_pubkey_input.strip() and not uploaded_file:
    st.info("▸  Public key loaded. Now upload a file to encrypt.")