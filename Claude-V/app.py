import streamlit as st
import json
import time
from datetime import datetime
from agents.scraper import fetch_new_pdfs, download_pdf
from agents.parser import extract_text_from_pdf
from agents.diff_agent import compute_diff
from agents.kb_agent import index_policy, query_policies
from agents.reasoning_agent import analyze_change, draft_amendment, simple_explain
from agents.report_agent import generate_report
from agents.voice_agent import text_to_speech_base64, get_language_options
from agents.chatbot_agent import chat_with_bot
from data.sample_data import SAMPLE_REGULATIONS, SAMPLE_POLICIES

st.set_page_config(
    page_title="RegIntel AI — Regulatory Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --gold: #D4A017;
    --gold-light: #F5E6A3;
    --navy: #0A1628;
    --navy-mid: #122040;
    --teal: #00B4A2;
    --teal-light: #80E8DF;
    --coral: #FF6B4A;
    --bg: #050E1C;
    --surface: #0D1F35;
    --surface2: #132840;
    --border: rgba(0,180,162,0.25);
    --text: #E8EDF5;
    --muted: #7A90A8;
}

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Headers */
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(0,180,162,0.15) !important;
}
[data-testid="stMetricValue"] {
    color: var(--teal) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), #007A70) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,180,162,0.3) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
}
.stTabs [aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom: 2px solid var(--teal) !important;
}

/* Info/success/warning blocks */
.stInfo { background: rgba(0,180,162,0.1) !important; border-left: 3px solid var(--teal) !important; border-radius: 8px !important; }
.stSuccess { background: rgba(80,200,120,0.1) !important; border-left: 3px solid #50C878 !important; border-radius: 8px !important; }
.stWarning { background: rgba(212,160,23,0.1) !important; border-left: 3px solid var(--gold) !important; border-radius: 8px !important; }

/* Code blocks */
code { background: var(--surface2) !important; color: var(--teal-light) !important; border-radius: 4px !important; }
pre { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--teal); border-radius: 3px; }

/* Alert badge */
.risk-high { color: #FF4D4D; font-weight: 700; background: rgba(255,77,77,0.1); padding: 2px 10px; border-radius: 20px; border: 1px solid rgba(255,77,77,0.3); }
.risk-medium { color: var(--gold); font-weight: 700; background: rgba(212,160,23,0.1); padding: 2px 10px; border-radius: 20px; border: 1px solid rgba(212,160,23,0.3); }
.risk-low { color: #50C878; font-weight: 700; background: rgba(80,200,120,0.1); padding: 2px 10px; border-radius: 20px; border: 1px solid rgba(80,200,120,0.3); }
</style>
""", unsafe_allow_html=True)

# ─── HERO HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0A1628 0%, #0D2A40 40%, #0A2030 100%);
    border: 1px solid rgba(0,180,162,0.3);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-60px;right:-60px;width:300px;height:300px;background:radial-gradient(circle,rgba(0,180,162,0.12),transparent 70%);border-radius:50%;"></div>
    <div style="position:absolute;bottom:-80px;left:100px;width:250px;height:250px;background:radial-gradient(circle,rgba(212,160,23,0.08),transparent 70%);border-radius:50%;"></div>
    <div style="display:flex;align-items:center;gap:1.5rem;margin-bottom:0.8rem;">
        <div style="font-size:3rem;filter:drop-shadow(0 0 16px rgba(0,180,162,0.5));">🛡️</div>
        <div>
            <h1 style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;margin:0;background:linear-gradient(90deg,#E8EDF5,#00B4A2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">RegIntel AI</h1>
            <p style="margin:0;color:#7A90A8;font-size:1rem;letter-spacing:0.1em;text-transform:uppercase;">Regulatory Intelligence Platform — RBI · SEBI · MCA</p>
        </div>
    </div>
    <p style="color:#A8C0D0;font-size:1rem;max-width:700px;margin:0;line-height:1.7;">
        AI-powered compliance monitoring that automatically tracks regulatory changes, maps impact to your policies, and generates actionable insights in real-time.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0;border-bottom:1px solid rgba(0,180,162,0.2);margin-bottom:1.5rem;">
        <div style="font-size:2rem;margin-bottom:0.3rem;">⚙️</div>
        <p style="font-family:'Syne',sans-serif;font-weight:700;margin:0;color:#E8EDF5;">Control Panel</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔄 Data Sources")
    rbi_enabled = st.checkbox("RBI Circulars", value=True)
    sebi_enabled = st.checkbox("SEBI Guidelines", value=True)
    mca_enabled = st.checkbox("MCA Notifications", value=True)

    st.markdown("---")
    st.markdown("### 🔊 Voice Bot Language")
    voice_lang = st.selectbox("Select Language", get_language_options())

    st.markdown("---")
    st.markdown("### 📊 Analysis Settings")
    risk_threshold = st.slider("Alert Risk Threshold", 1, 10, 7)
    auto_refresh = st.checkbox("Auto-refresh (24h)", value=False)

    st.markdown("---")
    if st.button("🚀 Run Full Pipeline", use_container_width=True):
        st.session_state["run_pipeline"] = True

    st.markdown("---")
    st.markdown("""
    <div style="padding:1rem;background:rgba(0,180,162,0.08);border-radius:12px;border:1px solid rgba(0,180,162,0.2);">
        <p style="font-size:0.75rem;color:#7A90A8;margin:0;text-align:center;">Last sync: just now<br>Next sync: 24h</p>
    </div>
    """, unsafe_allow_html=True)

# ─── METRICS ROW ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 Circulars Tracked", "247", "+12 this week")
c2.metric("⚠️ High-Risk Alerts", "8", "+2 today")
c3.metric("📁 Policies Indexed", "1,043", "+34")
c4.metric("⚡ Avg. Report Time", "4.2 min", "-0.8 min")

st.markdown("<br>", unsafe_allow_html=True)

# ─── MAIN TABS ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 Live Feed",
    "🔍 Analysis Engine",
    "💬 AI Chatbot",
    "🔊 Voice Assistant",
    "📊 Reports & Insights"
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — LIVE FEED
# ════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;color:#00B4A2;margin-bottom:0.3rem;">📡 Regulatory Live Feed</h2>
    <p style="color:#7A90A8;margin-bottom:1.5rem;">Real-time monitoring of RBI, SEBI, and MCA official portals</p>
    """, unsafe_allow_html=True)

    col_feed, col_detail = st.columns([1, 1])

    with col_feed:
        for reg in SAMPLE_REGULATIONS:
            risk_class = f"risk-{reg['risk'].lower()}"
            icon = "🔴" if reg['risk'] == "High" else ("🟡" if reg['risk'] == "Medium" else "🟢")
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0D1F35, #132840);
                border: 1px solid rgba(0,180,162,0.2);
                border-left: 4px solid {'#FF4D4D' if reg['risk']=='High' else ('#D4A017' if reg['risk']=='Medium' else '#50C878')};
                border-radius: 16px;
                padding: 1.2rem 1.5rem;
                margin-bottom: 1rem;
                cursor: pointer;
                transition: all 0.2s;
            ">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                    <span style="background:rgba(0,180,162,0.15);color:#00B4A2;font-size:0.75rem;font-weight:600;padding:2px 10px;border-radius:20px;border:1px solid rgba(0,180,162,0.3);">{reg['source']}</span>
                    <span class="{risk_class}">{icon} {reg['risk']}</span>
                </div>
                <p style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:600;color:#E8EDF5;margin:0.4rem 0;">{reg['title']}</p>
                <p style="font-size:0.82rem;color:#7A90A8;margin:0;">{reg['date']} · {reg['category']}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_detail:
        selected = SAMPLE_REGULATIONS[0]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D1F35,#132840);border:1px solid rgba(0,180,162,0.25);border-radius:16px;padding:1.5rem;">
            <h3 style="font-family:'Syne',sans-serif;color:#E8EDF5;margin-bottom:0.3rem;">{selected['title']}</h3>
            <p style="color:#7A90A8;font-size:0.85rem;margin-bottom:1rem;">{selected['source']} · {selected['date']}</p>
            <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:1rem;margin-bottom:1rem;">
                <p style="color:#A8C0D0;font-size:0.9rem;line-height:1.7;margin:0;">{selected['summary']}</p>
            </div>
            <div style="border-top:1px solid rgba(0,180,162,0.2);padding-top:1rem;">
                <p style="color:#7A90A8;font-size:0.8rem;margin:0 0 0.3rem;">KEY CHANGES DETECTED</p>
        """, unsafe_allow_html=True)
        st.code(selected.get('diff', '+ New clause added\n- Previous exemption removed'), language="diff")
        st.markdown("</div></div>", unsafe_allow_html=True)

        with st.expander("🤖 Auto-generated Impact Analysis"):
            st.markdown(f"""
            **Affected Modules:** Loan Processing, KYC Pipeline, Customer Onboarding  
            **Risk Assessment:** `HIGH` — Regulatory non-compliance may attract penalties  
            **Timeline:** Amendment required within 90 days  
            **Suggested Action:** Review Clause 3.1 of Loan Agreement; update internal SOP-KYC-001
            """)

# ════════════════════════════════════════════════════════════════
# TAB 2 — ANALYSIS ENGINE
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;color:#00B4A2;">🔍 Analysis Engine</h2>
    <p style="color:#7A90A8;margin-bottom:1.5rem;">Upload a regulation PDF or paste text to perform deep compliance analysis</p>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns([1, 1])

    with a1:
        st.markdown("#### 📄 Input Regulation")
        input_method = st.radio("Input Method", ["Use Sample Data", "Paste Text", "Upload PDF"], horizontal=True)

        if input_method == "Use Sample Data":
            selected_reg = st.selectbox("Select Regulation", [r['title'] for r in SAMPLE_REGULATIONS])
            reg_data = next(r for r in SAMPLE_REGULATIONS if r['title'] == selected_reg)
            reg_text = reg_data.get('full_text', reg_data['summary'])
        elif input_method == "Paste Text":
            reg_text = st.text_area("Paste Regulatory Text", height=200, placeholder="Paste the regulatory circular text here...")
        else:
            uploaded = st.file_uploader("Upload PDF", type="pdf")
            if uploaded:
                import tempfile, os
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded.read())
                    tmp_path = tmp.name
                reg_text = extract_text_from_pdf(tmp_path)
                st.success(f"✅ Extracted {len(reg_text.split())} words from PDF")
            else:
                reg_text = ""

        st.markdown("#### 📋 Compare with Previous Version")
        old_text = st.text_area("Previous Version (optional)", height=100, placeholder="Paste old version for diff analysis...")

        if st.button("⚡ Analyze Now", use_container_width=True):
            st.session_state["analyze"] = True
            st.session_state["reg_text"] = reg_text
            st.session_state["old_text"] = old_text

    with a2:
        if st.session_state.get("analyze") and st.session_state.get("reg_text"):
            reg_text = st.session_state["reg_text"]
            old_text = st.session_state.get("old_text", "")

            with st.spinner("🤖 Running AI analysis..."):
                time.sleep(0.5)
                if old_text:
                    diff = compute_diff(old_text, reg_text)
                else:
                    diff = reg_text

                hits = query_policies(reg_text[:500], k=3)
                context = "\n".join([h['text'][:200] for h in hits])
                analysis = analyze_change(diff[:1000], context)
                amendment = draft_amendment(diff[:800])
                simple = simple_explain(diff[:800])

            st.markdown("""
            <div style="background:rgba(80,200,120,0.08);border:1px solid rgba(80,200,120,0.3);border-radius:12px;padding:1rem;margin-bottom:1rem;">
                <p style="color:#50C878;font-size:0.8rem;font-weight:700;margin:0 0 0.3rem;">✅ ANALYSIS COMPLETE</p>
            """, unsafe_allow_html=True)

            with st.expander("📌 Impact Analysis", expanded=True):
                st.markdown(analysis)

            with st.expander("📝 Suggested Amendment"):
                st.markdown(amendment)

            with st.expander("💡 Plain-Language Explanation"):
                st.markdown(simple)

            with st.expander("🏛️ Matched Internal Policies"):
                for h in hits:
                    st.markdown(f"**{h.get('id','Policy')}** — {h['text'][:120]}...")

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#0D1F35,#132840);border:2px dashed rgba(0,180,162,0.3);border-radius:16px;padding:3rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;opacity:0.5;">🔍</div>
                <p style="color:#7A90A8;font-size:1rem;">Select a regulation and click <strong style="color:#00B4A2;">Analyze Now</strong> to generate AI-powered compliance insights</p>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — AI CHATBOT
# ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;color:#00B4A2;">💬 Regulatory Chatbot</h2>
    <p style="color:#7A90A8;margin-bottom:1.5rem;">Ask anything about RBI, SEBI, MCA regulations in natural language</p>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 Hello! I'm your RegIntel AI assistant. Ask me anything about RBI, SEBI, or MCA regulations — policy comparisons, compliance requirements, penalty clauses, filing deadlines, and more!"}
        ]

    # Chat container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin-bottom:0.8rem;">
                    <div style="background:linear-gradient(135deg,#00B4A2,#007A70);color:white;padding:0.8rem 1.2rem;border-radius:16px 16px 4px 16px;max-width:75%;font-size:0.9rem;line-height:1.6;">
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-start;margin-bottom:0.8rem;gap:0.8rem;align-items:flex-start;">
                    <div style="width:32px;height:32px;background:linear-gradient(135deg,#0D1F35,#132840);border:1px solid rgba(0,180,162,0.4);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0;">🛡️</div>
                    <div style="background:linear-gradient(135deg,#0D1F35,#122040);border:1px solid rgba(0,180,162,0.2);color:#E8EDF5;padding:0.8rem 1.2rem;border-radius:4px 16px 16px 16px;max-width:75%;font-size:0.9rem;line-height:1.6;">
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Quick suggestions
    st.markdown("<div style='margin-bottom:0.5rem;'>", unsafe_allow_html=True)
    sugg_cols = st.columns(3)
    suggestions = [
        "What are latest RBI KYC norms?",
        "SEBI IPO disclosure requirements?",
        "MCA annual filing deadlines 2024?"
    ]
    for i, (col, sug) in enumerate(zip(sugg_cols, suggestions)):
        with col:
            if st.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_input_val = sug

    # Input
    user_input = st.chat_input("Ask about regulations, compliance, filings, penalties...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Thinking..."):
            response = chat_with_bot(user_input, st.session_state.chat_history[-6:])
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# ════════════════════════════════════════════════════════════════
# TAB 4 — VOICE ASSISTANT
# ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;color:#00B4A2;">🔊 Voice Assistant</h2>
    <p style="color:#7A90A8;margin-bottom:1.5rem;">Get regulatory guidance in your preferred language via voice</p>
    """, unsafe_allow_html=True)

    v1, v2 = st.columns([1, 1])

    with v1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0D1F35,#132840);border:1px solid rgba(0,180,162,0.25);border-radius:20px;padding:2rem;text-align:center;">
            <div style="font-size:4rem;margin-bottom:1rem;animation:pulse 2s infinite;">🎙️</div>
            <h3 style="font-family:'Syne',sans-serif;color:#E8EDF5;margin-bottom:0.5rem;">Multilingual Voice Guide</h3>
            <p style="color:#7A90A8;font-size:0.9rem;margin-bottom:1.5rem;">Select a regulation and language. Our AI will explain it in audio format so anyone can understand it easily.</p>
        </div>
        """, unsafe_allow_html=True)

        voice_reg = st.selectbox("Select Regulation to Explain", [r['title'] for r in SAMPLE_REGULATIONS], key="voice_reg")
        lang_options = get_language_options()
        voice_language = st.selectbox("Language / भाषा / மொழி", lang_options, key="voice_lang_select")
        detail_level = st.radio("Detail Level", ["Brief Summary", "Detailed Explanation", "Key Action Points"], horizontal=True)

        if st.button("🔊 Generate Voice Explanation", use_container_width=True):
            reg_data = next(r for r in SAMPLE_REGULATIONS if r['title'] == voice_reg)
            with st.spinner(f"🎵 Generating audio in {voice_language}..."):
                audio_b64, transcript = text_to_speech_base64(
                    reg_data['summary'], voice_language, detail_level
                )
            st.session_state["voice_audio"] = audio_b64
            st.session_state["voice_transcript"] = transcript

    with v2:
        if st.session_state.get("voice_audio"):
            st.markdown("""
            <div style="background:linear-gradient(135deg,#0D1F35,#122040);border:1px solid rgba(0,180,162,0.25);border-radius:20px;padding:1.5rem;">
                <p style="color:#7A90A8;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;">🎵 Audio Ready</p>
            """, unsafe_allow_html=True)
            import base64
            audio_bytes = base64.b64decode(st.session_state["voice_audio"])
            st.audio(audio_bytes, format="audio/mp3")
            st.markdown("**Transcript:**")
            st.markdown(f"> {st.session_state['voice_transcript']}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#0D1F35,#132840);border:2px dashed rgba(0,180,162,0.25);border-radius:20px;padding:3rem;text-align:center;">
                <div style="font-size:3rem;margin-bottom:1rem;opacity:0.4;">🔊</div>
                <p style="color:#7A90A8;">Select a regulation and click <strong style="color:#00B4A2;">Generate Voice Explanation</strong></p>
                <p style="color:#7A90A8;font-size:0.8rem;margin-top:0.5rem;">Available in: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, English</p>
            </div>
            """, unsafe_allow_html=True)

    # Language cards
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🌐 Supported Languages")
    lang_grid = st.columns(4)
    langs = [
        ("🇮🇳", "Hindi", "हिंदी"),
        ("🇮🇳", "Tamil", "தமிழ்"),
        ("🇮🇳", "Telugu", "తెలుగు"),
        ("🇮🇳", "Bengali", "বাংলা"),
        ("🇮🇳", "Marathi", "मराठी"),
        ("🇮🇳", "Gujarati", "ગુજરાતી"),
        ("🇮🇳", "Kannada", "ಕನ್ನಡ"),
        ("🌐", "English", "English"),
    ]
    for i, (flag, name, native) in enumerate(langs):
        with lang_grid[i % 4]:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D1F35,#132840);border:1px solid rgba(0,180,162,0.2);border-radius:12px;padding:0.8rem;text-align:center;margin-bottom:0.8rem;">
                <div style="font-size:1.5rem;">{flag}</div>
                <p style="font-weight:600;color:#E8EDF5;margin:0.2rem 0 0;font-size:0.85rem;">{name}</p>
                <p style="color:#7A90A8;font-size:0.75rem;margin:0;">{native}</p>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 5 — REPORTS
# ════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;color:#00B4A2;">📊 Reports & Insights</h2>
    <p style="color:#7A90A8;margin-bottom:1.5rem;">Comprehensive compliance reports and trend analysis</p>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns([2, 1])

    with r1:
        st.markdown("#### 📈 Regulatory Activity Trend")
        import random
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
        rbi_counts = [12, 18, 15, 22, 19, 25, 21, 28, 24, 30]
        sebi_counts = [8, 11, 9, 14, 12, 16, 13, 18, 15, 20]
        mca_counts = [5, 7, 6, 9, 8, 10, 9, 12, 10, 14]

        import pandas as pd
        chart_data = pd.DataFrame({
            "RBI": rbi_counts,
            "SEBI": sebi_counts,
            "MCA": mca_counts
        }, index=months)
        st.line_chart(chart_data, use_container_width=True)

    with r2:
        st.markdown("#### ⚠️ Risk Distribution")
        risk_data = pd.DataFrame({"Count": [8, 23, 47]}, index=["High", "Medium", "Low"])
        st.bar_chart(risk_data, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Recent Compliance Reports")

    for reg in SAMPLE_REGULATIONS[:4]:
        with st.expander(f"{reg['source']} | {reg['title']} | {reg['date']}"):
            report = generate_report(
                reg['summary'],
                ["Loan Processing", "Customer Onboarding"],
                reg['risk'],
                "Review and update relevant policy documents within 30 days"
            )
            st.json(json.loads(report))

    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        report_json = generate_report("Consolidated monthly report", ["All modules"], "Medium", "Schedule compliance review")
        st.download_button(
            "⬇️ Download JSON Report",
            data=report_json,
            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            "⬇️ Download CSV Summary",
            data=pd.DataFrame(SAMPLE_REGULATIONS).to_csv(index=False),
            file_name=f"regulations_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
