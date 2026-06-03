import base64
import streamlit as st
from cryptography.hazmat.primitives import serialization

from crypto.aes_encryption import decrypt_data
from crypto.rsa_encryption import generate_rsa_keys, decrypt_key

st.set_page_config(page_title="CRYPTEX // RECEIVER", layout="wide", initial_sidebar_state="collapsed")

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
.cyber-header::after{content:'';position:absolute;bottom:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,var(--neon2),transparent);box-shadow:0 0 14px var(--neon2);}
.cyber-title{font-family:var(--hud);font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;color:var(--neon2);letter-spacing:6px;text-shadow:0 0 20px var(--neon2),0 0 60px rgba(255,0,60,0.4);animation:titlePulse2 3s ease-in-out infinite;}
@keyframes titlePulse2{0%,100%{text-shadow:0 0 20px var(--neon2),0 0 60px rgba(255,0,60,0.4);}50%{text-shadow:0 0 35px var(--neon2),0 0 90px rgba(255,0,60,0.65);}}
.cyber-sub{font-family:var(--vt);font-size:1.25rem;color:rgba(255,0,60,0.55);letter-spacing:4px;margin-top:0.4rem;animation:subtleBlink 1.8s step-end infinite;}
@keyframes subtleBlink{0%,100%{opacity:1;}50%{opacity:0.35;}}
.status-bar{display:flex;gap:1.5rem;flex-wrap:wrap;align-items:center;padding:0.5rem 1rem;margin:0.8rem 0;background:rgba(0,15,14,0.7);border:1px solid rgba(255,0,60,0.2);border-radius:3px;font-family:var(--mono);font-size:0.75rem;color:rgba(255,0,60,0.55);}
.s-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--neon2);box-shadow:0 0 8px var(--neon2);margin-right:6px;animation:dotBlink2 1.4s ease-in-out infinite;}
@keyframes dotBlink2{0%,100%{opacity:1;}50%{opacity:0.2;}}
.step-card{background:var(--panel);border:1px solid rgba(255,0,60,0.18);border-radius:4px;padding:0.9rem 1.3rem;margin:0.8rem 0;position:relative;overflow:hidden;animation:cardIn 0.45s cubic-bezier(0.23,1,0.32,1) both;transition:border-color 0.3s,box-shadow 0.3s;}
.step-card:hover{border-color:var(--neon2);box-shadow:0 0 22px rgba(255,0,60,0.15);}
.step-card.green{border-color:rgba(0,255,136,0.4)!important;background:rgba(0,20,12,0.92)!important;}
.step-card.green .step-label{color:#00ff88!important;}
.step-card.green .step-num{border-color:#00ff88!important;color:#00ff88!important;box-shadow:0 0 10px rgba(0,255,136,0.5)!important;}
.step-card.green::after{border-color:rgba(0,255,136,0.5)!important;}
.step-card.yellow{border-color:rgba(255,230,0,0.4)!important;background:rgba(18,15,0,0.92)!important;}
.step-card.yellow .step-label{color:var(--neon3)!important;}
.step-card.yellow .step-num{border-color:var(--neon3)!important;color:var(--neon3)!important;}
.step-card.yellow::after{border-color:rgba(255,230,0,0.5)!important;}
@keyframes cardIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
.step-card::before{content:'';position:absolute;top:0;left:-120%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,0,60,0.06),transparent);animation:shimmer 3s ease-in-out infinite;}
@keyframes shimmer{0%{left:-120%;}100%{left:220%;}}
.step-card::after{content:'';position:absolute;top:5px;right:5px;width:14px;height:14px;border-top:2px solid rgba(255,0,60,0.4);border-right:2px solid rgba(255,0,60,0.4);}
.step-label{font-family:var(--hud);font-size:0.68rem;font-weight:700;color:var(--neon2);letter-spacing:3px;text-transform:uppercase;display:flex;align-items:center;gap:0.7rem;margin-bottom:0.15rem;}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border:1.5px solid var(--neon2);border-radius:2px;font-size:0.65rem;color:var(--neon2);animation:numGlow2 2.5s ease-in-out infinite;}
@keyframes numGlow2{0%,100%{box-shadow:0 0 6px rgba(255,0,60,0.25);}50%{box-shadow:0 0 14px rgba(255,0,60,0.65);}}
.step-card .bl{position:absolute;bottom:5px;left:5px;width:12px;height:12px;border-bottom:2px solid rgba(255,0,60,0.3);border-left:2px solid rgba(255,0,60,0.3);}
code,pre,[data-testid="stCode"] pre{font-family:var(--mono)!important;font-size:0.8rem!important;background:rgba(255,0,60,0.04)!important;border:1px solid rgba(255,0,60,0.12)!important;border-radius:3px!important;color:#ff8099!important;line-height:1.65!important;animation:codeIn 0.35s ease both;}
@keyframes codeIn{from{opacity:0;transform:translateX(-6px);}to{opacity:1;transform:translateX(0);}}
.stButton>button{font-family:var(--hud)!important;font-size:0.82rem!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;color:#fff!important;background:var(--neon2)!important;border:none!important;border-radius:2px!important;padding:0.6rem 2rem!important;box-shadow:0 0 18px rgba(255,0,60,0.7),0 3px 0 rgba(150,0,30,0.9)!important;transition:all 0.15s ease!important;position:relative!important;overflow:hidden!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 32px rgba(255,0,60,0.95),0 5px 0 rgba(150,0,30,0.9)!important;}
.stButton>button:active{transform:translateY(1px)!important;}
textarea{background:rgba(8,0,5,0.88)!important;border:1px solid rgba(255,0,60,0.25)!important;border-radius:3px!important;color:#ffaabb!important;font-family:var(--mono)!important;font-size:0.8rem!important;transition:border-color 0.3s,box-shadow 0.3s!important;}
textarea:focus{border-color:var(--neon2)!important;box-shadow:0 0 16px rgba(255,0,60,0.3)!important;}
label{font-family:var(--hud)!important;color:var(--neon2)!important;font-size:0.72rem!important;letter-spacing:2px!important;}
.stProgress>div{background:rgba(255,0,60,0.08)!important;border-radius:2px!important;height:6px!important;border:1px solid rgba(255,0,60,0.12)!important;}
.stProgress>div>div{background:linear-gradient(90deg,var(--neon2),#ff8800)!important;box-shadow:0 0 12px var(--neon2)!important;border-radius:2px!important;transition:width 0.7s cubic-bezier(0.4,0,0.2,1)!important;}
[data-testid="stAlert"]{background:rgba(255,0,60,0.05)!important;border:1px solid var(--neon2)!important;border-radius:3px!important;box-shadow:0 0 20px rgba(255,0,60,0.12)!important;}
[data-testid="stAlert"] *{color:#ff8099!important;font-family:var(--mono)!important;}
[data-testid="stDownloadButton"]>button{font-family:var(--hud)!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;background:transparent!important;border:2px solid var(--neon)!important;color:var(--neon)!important;border-radius:2px!important;padding:0.55rem 1.5rem!important;box-shadow:0 0 12px rgba(0,255,231,0.35)!important;transition:all 0.2s ease!important;}
[data-testid="stDownloadButton"]>button:hover{background:rgba(0,255,231,0.08)!important;box-shadow:0 0 28px rgba(0,255,231,0.7)!important;transform:translateY(-2px)!important;}
hr{border-color:rgba(255,0,60,0.12)!important;}
p,span,[data-testid="stMarkdownContainer"] *{font-family:var(--mono)!important;color:var(--text)!important;}
h1{font-family:var(--hud)!important;color:var(--neon2)!important;text-shadow:0 0 18px var(--neon2)!important;letter-spacing:4px;}
h2,h3{font-family:var(--hud)!important;color:var(--neon2)!important;letter-spacing:2px;font-size:0.95rem!important;}
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
    x.strokeStyle='rgba(255,0,60,0.03)';x.lineWidth=.5;
    for(let i=0;i<c.width;i+=PX){x.beginPath();x.moveTo(i,0);x.lineTo(i,c.height);x.stroke();}
    for(let i=0;i<c.height;i+=PX){x.beginPath();x.moveTo(0,i);x.lineTo(c.width,i);x.stroke();}
    x.fillStyle='rgba(255,0,60,0.08)';
    for(let i=0;i<c.width;i+=PX)for(let j=0;j<c.height;j+=PX)x.fillRect(i-1,j-1,2,2);
    x.font=FS+'px "Share Tech Mono",monospace';
    for(let i=0;i<cols;i++){
      const ch=CH[Math.floor(Math.random()*CH.length)],yy=drops[i]*FS;
      x.fillStyle='rgba(255,180,190,0.7)';x.fillText(ch,i*FS,yy);
      x.fillStyle='rgba(255,0,60,0.13)';x.fillText(CH[Math.floor(Math.random()*CH.length)],i*FS,yy-FS*2);
      x.fillStyle='rgba(200,0,40,0.07)';x.fillText(CH[Math.floor(Math.random()*CH.length)],i*FS,yy-FS*5);
      drops[i]++;if(drops[i]*FS>c.height&&Math.random()>.975)drops[i]=0;
    }
    nodes.forEach((p,i)=>{
      p.x+=p.vx;p.y+=p.vy;p.ph+=0.025;
      if(p.x<0||p.x>c.width)p.vx*=-1;if(p.y<0||p.y>c.height)p.vy*=-1;
      const g=.5+.5*Math.sin(p.ph);
      nodes.forEach((q,j)=>{if(j<=i)return;const d=Math.hypot(p.x-q.x,p.y-q.y);if(d<120){x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.strokeStyle=`rgba(255,0,60,${(1-d/120)*.16*g})`;x.lineWidth=.7;x.stroke();}});
      x.beginPath();x.arc(p.x,p.y,p.r*(0.7+0.5*g),0,Math.PI*2);x.fillStyle=`rgba(255,0,60,${0.4+0.6*g})`;x.shadowBlur=10;x.shadowColor='#ff003c';x.fill();x.shadowBlur=0;
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
  <div class="cyber-title">⬡ CRYPTEX // RECEIVER</div>
  <div class="cyber-sub">[ DECRYPTION TERMINAL ]</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">
  <span><span class="s-dot"></span>RECEIVER NODE ONLINE</span>
  <span>NODE: COMPUTER B</span>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS EXPLAINER ──────────────────────────────────────────────────
st.markdown("""
<div class="step-card yellow">
  <div class="step-label"><span class="step-num">ℹ</span>HOW THIS WORKS — READ FIRST</div>
  <div class="bl"></div>
  <p style="color:rgba(255,230,0,0.8);font-size:0.82rem;margin-top:0.5rem;line-height:1.8;">
    STEP A → You generate your RSA key pair here on Computer B<br>
    STEP B → You copy your PUBLIC KEY and send it to Computer A (Sender)<br>
    STEP C → Sender uploads the file, encrypts it, and uses YOUR public key to lock the AES key<br>
    STEP D → Sender gives you: Encrypted File + Encrypted AES Key<br>
    STEP E → You paste those here and decrypt using YOUR private key (which never left this machine)
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
#  PHASE A — GENERATE RSA KEY PAIR (stored in session, private key never leaves)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card green">
  <div class="step-label"><span class="step-num">A</span>GENERATE YOUR RSA KEY PAIR</div>
  <div class="bl"></div>
</div>
""", unsafe_allow_html=True)

if st.button("⬡ GENERATE MY RSA KEY PAIR"):
    priv_obj, pub_obj = generate_rsa_keys()
    st.session_state["priv_pem"] = priv_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    st.session_state["pub_pem"] = pub_obj.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

if "pub_pem" in st.session_state:

    st.markdown("""
    <div class="step-card green">
      <div class="step-label"><span class="step-num">✓</span>KEY PAIR GENERATED AND STORED IN SESSION</div>
      <div class="bl"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="color:#00ff88;font-family:Orbitron,monospace;font-size:0.72rem;letter-spacing:2px;margin-bottom:4px;">▸ PUBLIC KEY — COPY THIS, SEND TO SENDER</p>', unsafe_allow_html=True)
        st.code(st.session_state["pub_pem"])

    with col2:
        st.markdown('<p style="color:#ffe600;font-family:Orbitron,monospace;font-size:0.72rem;letter-spacing:2px;margin-bottom:4px;">🔒 PRIVATE KEY — STORED HERE, NEVER SHARED</p>', unsafe_allow_html=True)
        st.code(st.session_state["priv_pem"])

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    #  PHASE B — PASTE PAYLOAD FROM SENDER & DECRYPT
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="step-card">
      <div class="step-label"><span class="step-num">B</span>PASTE ENCRYPTED PAYLOAD FROM SENDER</div>
      <div class="bl"></div>
    </div>
    """, unsafe_allow_html=True)

    enc_data = st.text_area("① ENCRYPTED FILE DATA",  height=110, placeholder="Paste the encrypted file data that the sender gave you...")
    enc_key  = st.text_area("② ENCRYPTED AES KEY",    height=75,  placeholder="Paste the encrypted AES key that the sender gave you...")

    st.markdown("")

    if st.button("⬡ DECRYPT FILE"):
        progress = st.progress(0)
        try:
            # Load private key from session — it never left this machine
            priv_key = serialization.load_pem_private_key(
                st.session_state["priv_pem"].encode(), password=None
            )
            progress.progress(25)

            st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">C</span>USING YOUR PRIVATE KEY TO UNLOCK THE AES KEY...</div><div class="bl"></div></div>""", unsafe_allow_html=True)
            aes_key = decrypt_key(base64.b64decode(enc_key.strip()), priv_key)
            progress.progress(60)

            st.markdown("""<div class="step-card"><div class="step-label"><span class="step-num">D</span>USING AES KEY TO DECRYPT THE FILE...</div><div class="bl"></div></div>""", unsafe_allow_html=True)
            decrypted_data = decrypt_data(base64.b64decode(enc_data.strip()), aes_key)
            progress.progress(100)

            st.success("▶  FILE SUCCESSFULLY DECRYPTED")
            st.code(decrypted_data[:300])
            st.download_button(
                label="⬇  DOWNLOAD RECOVERED FILE",
                data=decrypted_data,
                file_name="recovered_file.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("⚠  DECRYPTION FAILED — ENSURE YOU USED THE CORRECT PAYLOAD")
            st.code(str(e))