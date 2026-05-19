import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# --- Page Setup ---
st.set_page_config(
    page_title="Gallery AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.2rem 2.5rem 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* ── App Background ── */
.stApp {
    background-color: #0C0C0E;
    color: #E8E6DF;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #111115 !important;
    border-right: 1px solid #1F1F28 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.4rem !important;
}
[data-testid="stSidebar"] * {
    color: #E8E6DF !important;
}

/* ── Brand ── */
.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 1.6rem;
    margin-bottom: 1.6rem;
    border-bottom: 1px solid #1F1F28;
}
.brand-glyph {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    color: #C8F06A;
    line-height: 1;
    letter-spacing: -2px;
}
.brand-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #E8E6DF;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.brand-tag {
    font-size: 0.65rem;
    color: #555560;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 1px;
}

/* ── Sidebar section labels ── */
.slabel {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #C8F06A;
    margin: 1.4rem 0 0.6rem 0;
    display: block;
}

/* ── Sidebar divider ── */
.sdivide {
    border: none;
    border-top: 1px solid #1F1F28;
    margin: 1.4rem 0;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #2A2A35 !important;
    border-radius: 6px !important;
    background: #16161D !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #C8F06A !important;
}
[data-testid="stFileUploader"] * {
    color: #888895 !important;
    font-size: 0.8rem !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input {
    background: #16161D !important;
    border: 1px solid #2A2A35 !important;
    border-radius: 6px !important;
    color: #E8E6DF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.84rem !important;
    padding: 0.5rem 0.8rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #C8F06A !important;
    box-shadow: 0 0 0 1px #C8F06A22 !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #44444F !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #C8F06A !important;
    color: #0C0C0E !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: #16161D !important;
    border: 1px solid #2A2A35 !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    color: #E8E6DF !important;
}

/* ── Main page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding-bottom: 1.4rem;
    margin-bottom: 1.8rem;
    border-bottom: 1px solid #1F1F28;
}
.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.55rem;
    font-weight: 700;
    color: #E8E6DF;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.page-title span {
    color: #C8F06A;
}
.page-desc {
    font-size: 0.8rem;
    color: #44444F;
    margin-top: 5px;
    letter-spacing: 0.02em;
}
.page-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #C8F06A;
    border: 1px solid #C8F06A33;
    border-radius: 4px;
    padding: 4px 10px;
    background: #C8F06A0A;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.5rem 0 !important;
    gap: 12px !important;
}
[data-testid="stChatMessageContent"] {
    font-size: 0.88rem !important;
    line-height: 1.75 !important;
    color: #D4D2CB !important;
}

/* ── Avatars ── */
[data-testid="chatAvatarIcon-assistant"] {
    background: #C8F06A !important;
    border-radius: 4px !important;
    color: #0C0C0E !important;
    font-size: 0.75rem !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #1F1F28 !important;
    border-radius: 4px !important;
    color: #888895 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #111115 !important;
    border: 1px solid #2A2A35 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #C8F06A !important;
    box-shadow: 0 0 0 2px #C8F06A11 !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    color: #E8E6DF !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #33333D !important;
}

/* ── Meta pills ── */
.meta-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #1F1F28;
}
.meta-pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.06em;
    background: #16161D;
    border: 1px solid #2A2A35;
    border-radius: 3px;
    padding: 3px 8px;
    color: #666672;
}
.meta-pill-accent {
    color: #C8F06A;
    border-color: #C8F06A33;
    background: #C8F06A08;
}

/* ── Source item in sidebar ── */
.src-item {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 5px 8px;
    background: #16161D;
    border: 1px solid #1F1F28;
    border-radius: 5px;
    margin-bottom: 4px;
    font-size: 0.75rem;
    color: #888895;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.src-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #C8F06A;
    flex-shrink: 0;
}

/* ── Sidebar footer ── */
.sfooter {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2E2E3A;
    margin-top: 2rem;
    line-height: 2;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0C0C0E; }
::-webkit-scrollbar-thumb { background: #1F1F28; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div class="brand-wrap">
        <div class="brand-glyph">◈</div>
        <div>
            <div class="brand-name">Gallery AI</div>
            <div class="brand-tag">Knowledge Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PDF ──────────────────────────────
    st.markdown('<span class="slabel">// Document</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop PDF", type=["pdf"], label_visibility="collapsed"
    )
    if st.button("Ingest PDF →", key="btn_pdf"):
        if uploaded_file:
            with st.spinner("Parsing…"):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{API_BASE_URL}/admin/ingest-pdf", files=files)
                    if res.status_code == 200:
                        n = res.json().get("chunks_ingested", "?")
                        st.success(f"✓ {uploaded_file.name} — {n} chunks")
                    else:
                        st.error("Ingestion failed.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("No file selected.")

    st.markdown('<hr class="sdivide">', unsafe_allow_html=True)

    # ── URL ──────────────────────────────
    st.markdown('<span class="slabel">// Web</span>', unsafe_allow_html=True)
    input_url = st.text_input("URL", placeholder="https://example.com", label_visibility="collapsed")
    if st.button("Ingest URL →", key="btn_url"):
        if input_url:
            with st.spinner("Fetching…"):
                try:
                    res = requests.post(f"{API_BASE_URL}/admin/ingest-url", json={"url": input_url})
                    if res.status_code == 200:
                        n = res.json().get("chunks_ingested", "?")
                        st.success(f"✓ Indexed — {n} chunks")
                    else:
                        st.error("Scraping failed.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Enter a URL first.")

    st.markdown('<hr class="sdivide">', unsafe_allow_html=True)

    # ── Sources ──────────────────────────
    st.markdown('<span class="slabel">// Sources</span>', unsafe_allow_html=True)
    if st.button("Refresh →", key="btn_src"):
        try:
            res = requests.get(f"{API_BASE_URL}/admin/sources")
            st.session_state["kb_sources"] = res.json().get("sources", []) if res.status_code == 200 else []
        except:
            st.session_state["kb_sources"] = []

    if "kb_sources" in st.session_state:
        srcs = st.session_state["kb_sources"]
        if srcs:
            for s in srcs:
                label = s.split("/")[-1] if "/" in s else s
                st.markdown(f'<div class="src-item"><span class="src-dot"></span>{label}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.75rem;color:#33333D;padding:4px 0;">No sources yet.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sfooter">
        RAG · MMR · ChromaDB<br>
        GPT-4o mini<br>
        © Gallery AI
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════

st.markdown("""
<div class="page-header">
    <div>
        <div class="page-title">Ask your <span>knowledge base</span></div>
        <div class="page-desc">Add a PDF or URL via the sidebar — then interrogate it.</div>
    </div>
    <div class="page-badge">◈ RAG · Online</div>
</div>
""", unsafe_allow_html=True)

# ── Session ──────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "System ready. Upload a document or paste a URL in the sidebar to seed the knowledge base. Then ask anything.",
        "topic": None,
        "sources": []
    }]

# ── History ──────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and (msg.get("topic") or msg.get("sources")):
            pills = '<div class="meta-wrap">'
            if msg.get("topic"):
                pills += f'<span class="meta-pill meta-pill-accent">{msg["topic"]}</span>'
            for s in (msg.get("sources") or []):
                lbl = s.split("/")[-1] if "/" in s else s
                pills += f'<span class="meta-pill">{lbl}</span>'
            pills += '</div>'
            st.markdown(pills, unsafe_allow_html=True)

# ── Input ─────────────────────────────
if prompt := st.chat_input("Query the knowledge base…"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "topic": None, "sources": []})

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                res = requests.post(f"{API_BASE_URL}/query", json={"question": prompt})
                if res.status_code == 200:
                    data = res.json()
                    answer  = data.get("answer", "No answer returned.")
                    topic   = data.get("topic", "")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    if topic or sources:
                        pills = '<div class="meta-wrap">'
                        if topic:
                            pills += f'<span class="meta-pill meta-pill-accent">{topic}</span>'
                        for s in sources:
                            lbl = s.split("/")[-1] if "/" in s else s
                            pills += f'<span class="meta-pill">{lbl}</span>'
                        pills += '</div>'
                        st.markdown(pills, unsafe_allow_html=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "topic": topic,
                        "sources": sources
                    })
                else:
                    st.error("Engine unavailable. Try again later.")
            except Exception as e:
                st.error(f"Cannot reach backend. Is main.py running? ({e})")
