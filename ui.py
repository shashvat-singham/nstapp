"""Shared UI theme for the StyleGenix app (injected CSS + small helpers)."""
import streamlit as st

_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

/* Hide default Streamlit chrome for a cleaner look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stDecoration"] {display: none;}

html, body, [class*="css"], .stMarkdown, p, span, label, input, div {
    font-family: 'Poppins', sans-serif;
}

/* Animated gradient background */
.stApp {
    background:
        radial-gradient(1100px 550px at 8% 6%, rgba(139,92,246,0.28), transparent 60%),
        radial-gradient(900px 500px at 92% 92%, rgba(236,72,153,0.24), transparent 60%),
        linear-gradient(135deg, #140b2e 0%, #241458 48%, #3a1c6e 100%);
    background-attachment: fixed;
}

.block-container {
    max-width: 820px;
    padding-top: 2.4rem;
    padding-bottom: 4rem;
}

/* ---------- Hero ---------- */
.sg-hero { text-align: center; margin: .4rem 0 1.6rem; }
.sg-logo {
    display: inline-flex; align-items: center; justify-content: center;
    width: 74px; height: 74px; border-radius: 22px; font-size: 2.2rem;
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    box-shadow: 0 14px 34px rgba(139,92,246,.45);
    margin-bottom: .8rem;
}
.sg-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.7rem; font-weight: 800; line-height: 1.1; margin: 0;
    background: linear-gradient(90deg, #c4b5fd, #f5d0fe, #a5b4fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.sg-sub {
    color: #cbd5e1; font-weight: 300; font-size: 1.02rem;
    margin-top: .5rem; max-width: 560px; margin-left: auto; margin-right: auto;
}

/* ---------- Glass card (forms) ---------- */
form[data-testid="stForm"] {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 22px;
    padding: 1.8rem 1.8rem 1.2rem;
    box-shadow: 0 24px 70px rgba(0,0,0,0.38);
}

/* Generic glass panel helper */
.sg-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 1.4rem 1.5rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.32);
}

/* ---------- Inputs ---------- */
.stTextInput input, .stTextInput input:focus, .stNumberInput input {
    background: rgba(255,255,255,0.06);
    color: #f8fafc;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 12px;
    padding: .72rem .95rem;
}
.stTextInput input:focus {
    border-color: #a78bfa;
    box-shadow: 0 0 0 3px rgba(167,139,250,.28);
}
.stTextInput label, .stFileUploader label, .stRadio label,
.stTextInput label p, label p {
    color: #e5e7eb !important; font-weight: 500;
}
.stTextInput input::placeholder { color: #94a3b8; }

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    width: 100%;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    color: #fff; border: none; border-radius: 12px;
    padding: .72rem 1rem; font-weight: 600; font-size: 1rem;
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
    box-shadow: 0 12px 26px rgba(139,92,246,.38);
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 34px rgba(236,72,153,.48);
    filter: brightness(1.05);
}
.stButton > button:active, .stFormSubmitButton > button:active { transform: translateY(0); }

/* ---------- Radio as segmented pills ---------- */
div[role="radiogroup"] {
    display: flex; gap: .4rem; justify-content: center; flex-wrap: wrap;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: .38rem; border-radius: 14px; margin: 0 auto 1.3rem;
    width: fit-content;
}
div[role="radiogroup"] > label {
    margin: 0 !important; padding: .5rem 1.1rem; border-radius: 10px;
    cursor: pointer; color: #cbd5e1; font-weight: 500;
    transition: all .15s ease;
}
div[role="radiogroup"] > label:hover { color: #fff; background: rgba(255,255,255,0.06); }
div[role="radiogroup"] > label > div:first-child { display: none; }  /* hide radio dot */
div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    color: #fff; box-shadow: 0 8px 20px rgba(139,92,246,.4);
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.05);
    border: 1.5px dashed rgba(167,139,250,0.5);
    border-radius: 16px;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #a78bfa; background: rgba(167,139,250,0.08);
}

/* ---------- Images ---------- */
[data-testid="stImage"] img { border-radius: 14px; }

/* ---------- Alerts ---------- */
.stAlert { border-radius: 14px; }

/* ---------- Section heading ---------- */
.sg-section {
    font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.15rem;
    color: #f1f5f9; margin: 1.4rem 0 .6rem;
}

/* ---------- Footer ---------- */
.sg-footer {
    text-align: center; color: #94a3b8; font-size: .85rem;
    margin-top: 2.2rem; font-weight: 300;
}
.sg-footer b { color: #c4b5fd; }

/* Sidebar polish */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,11,46,0.9), rgba(36,20,88,0.9));
    border-right: 1px solid rgba(255,255,255,0.08);
}
</style>
"""


def inject_theme():
    """Inject the global StyleGenix theme. Call once per page."""
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def hero(title, subtitle, logo="🎨"):
    """Render the centered brand hero."""
    st.markdown(
        f"""
        <div class="sg-hero">
            <div class="sg-logo">{logo}</div>
            <h1 class="sg-title">{title}</h1>
            <p class="sg-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<div class="sg-footer">Made with ❤️ by <b>StyleGenix</b> · Neural Style Transfer</div>',
        unsafe_allow_html=True,
    )
