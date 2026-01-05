import streamlit as st
import os
from dotenv import load_dotenv

# --- CONFIGURATION MUST BE FIRST ---
st.set_page_config(
    page_title="NEXUS | Enterprise AI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv() # Load keys

# --- IMPORT YOUR MODULES ---
from ingest import IngestEngine
from database import DatabaseManager

# ==========================================
# 🎨 UI DESIGN: CYBER-BHARAT THEME (FIXED VISIBILITY)
# ==========================================
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&family=Fira+Code:wght@400;600&display=swap');

    /* 1. GLOBAL BACKGROUND - "Deep Cosmos" */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a0b2e 0%, #0f0c29 100%);
        color: #E0E0E0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* 2. SIDEBAR - TECH DARK */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0f19 0%, #111625 100%);
        border-right: 1px solid #FF9933;
        box-shadow: 5px 0 15px rgba(255, 153, 51, 0.1);
    }

    /* 3. HEADERS - TRICOLOR GRADIENT */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: -webkit-linear-gradient(0deg, #FF9933 10%, #FFFFFF 50%, #138808 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(255, 153, 51, 0.3);
    }

    /* 4. CHAT BUBBLES - HIGH CONTRAST TEXT FIX */
    .stChatMessage {
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* FORCE TEXT COLOR TO WHITE FOR READABILITY */
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #FFFFFF !important; 
        font-weight: 500 !important; /* Slightly bolder text */
        text-shadow: 0 1px 2px rgba(0,0,0,0.5); /* Shadow to make text pop */
    }

    /* USER: GOLD/SAFFRON GLASS */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(255, 153, 51, 0.2) 0%, rgba(255, 153, 51, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 153, 51, 0.5);
        border-left: 5px solid #FF9933;
    }

    /* AI: ELECTRIC CYAN/BLUE GLASS */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(0, 201, 255, 0.2) 0%, rgba(0, 201, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 201, 255, 0.5);
        border-left: 5px solid #00C9FF;
    }

    /* 5. CUSTOM BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #e52d27 0%, #000080 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(229, 45, 39, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 128, 0.6);
        color: #fff;
    }

    /* 6. FILE UPLOADER */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #FF9933;
        border-radius: 12px;
        padding: 10px;
        background: rgba(255, 153, 51, 0.05);
    }
    div.stChatInput {
        border-color: #00C9FF !important;
    }
    
    /* 7. TOP RIGHT MENU */
    button[data-testid="stBaseButton-header"] {
        color: #FF9933 !important;
    }
    div[data-testid="stToolbar"] {
        color: #00C9FF !important;
    }

    /* 8. CODE BLOCKS */
    code {
        font-family: 'Fira Code', monospace !important;
        background-color: #121212 !important;
        color: #00C9FF !important;
        border: 1px solid #333;
    }
    
    /* 9. LOGO ANIMATION */
    @keyframes spin-glow {
        0% { box-shadow: 0 0 5px #FF9933; }
        50% { box-shadow: 0 0 20px #FFFFFF; }
        100% { box-shadow: 0 0 5px #138808; }
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo-circle {
        width: 90px;
        height: 90px;
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 45px;
        animation: spin-glow 3s infinite alternate;
        color: #000080;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        border: 4px solid #000080;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 APP LOGIC
# ==========================================

# 1. Title & Status
st.title("⚡ NEXUS")
st.caption("INTELLIGENCE ENGINE | STATUS: ONLINE")
st.markdown("---")

# 2. Initialize State
if "db" not in st.session_state: st.session_state.db = DatabaseManager()
if "ingest" not in st.session_state: st.session_state.ingest = IngestEngine()
if "history" not in st.session_state: st.session_state.history = []

# 3. Sidebar Logic
with st.sidebar:
    # Custom Logo
    st.markdown("""
        <div class="logo-container">
            <div class="logo-circle">N</div>
        </div>
        <h3 style="text-align: center; letter-spacing: 4px; font-size: 24px;">NEXUS</h3>
        <p style="text-align: center; color: #aaa; font-size: 12px;">Made in India 🇮🇳</p>
    """, unsafe_allow_html=True)
    
    st.header("📂 Ingestion Deck")
    uploaded = st.file_uploader("Upload Schematics (PDF)", type="pdf")
    
    if uploaded and st.button("🚀 Initialize Upload"):
        with st.status("⚙️ Processing Data Matrix...", expanded=True) as status:
            st.write("🔹 Scanning Vector Embeddings...")
            with open("temp.pdf", "wb") as f: f.write(uploaded.getbuffer())
            success, msg = st.session_state.ingest.process_pdf("temp.pdf")
            if success:
                status.update(label="✅ Upload Complete", state="complete", expanded=False)
                st.success(msg)
            else:
                status.update(label="❌ Upload Failed", state="error")
                st.error(msg)
    
    st.markdown("---")
    st.info("Mode: Engineer | Model: Gemini-2.5-Flash")

# 4. Chat History
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "images" in msg and msg["images"]:
            cols = st.columns(len(msg["images"]))
            for idx, img in enumerate(msg["images"]):
                if os.path.exists(img):
                    with cols[idx]:
                        st.image(img, caption=f"Figure {idx+1}", use_container_width=True)
        if "tables" in msg and msg["tables"]:
            for tbl in msg["tables"]:
                with st.expander("📊 View Extracted Data"):
                    st.markdown(tbl, unsafe_allow_html=True)

# 5. Chat Input
if prompt := st.chat_input("Enter command..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("🔄 Neural Processing..."):
            reply, imgs, tbls = st.session_state.db.ask_ai(prompt)
            message_placeholder.write(reply)
            
            if imgs:
                st.markdown("### 🖼️ Visual Data")
                img_cols = st.columns(min(len(imgs), 3))
                for i, img in enumerate(imgs):
                    if os.path.exists(img):
                        with img_cols[i % 3]:
                            st.image(img, caption="Source Figure", use_container_width=True)
            
            if tbls:
                st.markdown("### 📊 Data Arrays")
                for tbl in tbls:
                    with st.expander("View Data Table", expanded=False):
                        st.markdown(tbl, unsafe_allow_html=True)

            st.session_state.history.append({
                "role": "assistant", 
                "content": reply, 
                "images": imgs, 
                "tables": tbls
            })