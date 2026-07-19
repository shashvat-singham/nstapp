import base64
import hashlib
from io import BytesIO

import streamlit as st
from PIL import Image
import numpy as np
import pyrebase

# NOTE: TensorFlow / TF-Hub (via API.py) is imported lazily inside the block
# that needs it, so opening this page stays instant.

# ---------------------------------------------------------------------------
# Firebase (Realtime Database) — same project as the auth page
# ---------------------------------------------------------------------------
firebase_config = {
    "apiKey": "AIzaSyDJiQuv0cZ-AiObYbtQHhtTABhLm-Smxrg",
    "authDomain": "stylegenix-b8eed.firebaseapp.com",
    "projectId": "stylegenix-b8eed",
    "storageBucket": "stylegenix-b8eed.appspot.com",
    "messagingSenderId": "835045766386",
    "appId": "1:835045766386:web:3fe54f2c171b1fa303cc6b",
    "measurementId": "G-LX246R50J9",
    "databaseURL": "https://stylegenix-b8eed.firebaseio.com",
}


@st.cache_resource(show_spinner=False)
def get_db():
    return pyrebase.initialize_app(firebase_config).database()


def _auth():
    """Return (uid, id_token) of the logged-in user, or (None, None)."""
    return st.session_state.get("uid"), (
        st.session_state.get("id_token") or st.session_state.get("user")
    )


def _thumb_b64(pil_img, max_side=512, quality=80):
    """Downscale to a thumbnail and return base64-encoded JPEG (for RTDB)."""
    img = pil_img.convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def save_creation(content_img, style_img, result_img):
    """Store this creation under users/{uid}/creations in the Realtime DB."""
    uid, token = _auth()
    if not uid:
        return False, "Please log out and sign in again to enable saving."
    try:
        get_db().child("users").child(uid).child("creations").push(
            {
                "content": _thumb_b64(content_img),
                "style": _thumb_b64(style_img),
                "result": _thumb_b64(result_img),
                "created_at": {".sv": "timestamp"},
            },
            token,
        )
        return True, None
    except Exception as e:
        return False, str(e)


def load_creations():
    """Return this user's creations, newest first."""
    uid, token = _auth()
    if not uid:
        return []
    try:
        snap = get_db().child("users").child(uid).child("creations").get(token)
        items = [c.val() for c in (snap.each() or [])]
        return list(reversed(items))
    except Exception:
        return []


@st.cache_data(show_spinner=False)
def stylize(content_bytes, style_bytes, max_dim):
    """Run neural style transfer. Cached so reruns (e.g. clicking download)
    don't recompute or re-import TensorFlow. Higher max_dim = more detail."""
    from API import transfer_style  # lazy import (loads TensorFlow only now)

    content_arr = np.array(Image.open(BytesIO(content_bytes)).convert("RGB"))
    style_arr = np.array(Image.open(BytesIO(style_bytes)).convert("RGB"))
    return transfer_style(content_arr, style_arr, r"model", max_dim=max_dim)


def logout():
    for k in ("user", "id_token", "uid", "email"):
        st.session_state.pop(k, None)
    st.session_state["redirect_to_auth"] = True
    st.rerun()


# ---------------------------------------------------------------------------
# Auth gate
# ---------------------------------------------------------------------------
if st.session_state.get("redirect_to_auth"):
    st.session_state.clear()
    st.session_state["redirect"] = True
    st.rerun()

if "user" not in st.session_state:
    st.warning("Please log in to access this page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page config + theme
# ---------------------------------------------------------------------------
st.set_page_config(page_title="StyleGenix · Studio", page_icon="🎨", layout="wide")

_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stDecoration"] {display: none;}
[data-testid="InputInstructions"] {display: none;}

html, body, [class*="css"], .stMarkdown, p, span, label, input, div {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(1100px 550px at 8% 6%, rgba(139,92,246,0.28), transparent 60%),
        radial-gradient(900px 500px at 92% 92%, rgba(236,72,153,0.24), transparent 60%),
        linear-gradient(135deg, #140b2e 0%, #241458 48%, #3a1c6e 100%);
    background-attachment: fixed;
}
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1050px; }

.sg-hero { text-align: center; margin: .2rem 0 1.4rem; }
.sg-logo {
    display:inline-flex; align-items:center; justify-content:center;
    width:64px; height:64px; border-radius:20px; font-size:1.9rem;
    background: linear-gradient(135deg,#8b5cf6,#ec4899);
    box-shadow: 0 14px 34px rgba(139,92,246,.45); margin-bottom:.6rem;
}
.sg-title {
    font-family:'Sora',sans-serif; font-size:2.4rem; font-weight:800; margin:0;
    background: linear-gradient(90deg,#c4b5fd,#f5d0fe,#a5b4fc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:-.5px;
}
.sg-sub { color:#cbd5e1; font-weight:300; font-size:1rem; margin-top:.4rem; }

.sg-step {
    font-family:'Sora',sans-serif; font-weight:700; font-size:1.05rem; color:#f1f5f9;
    margin:1rem 0 .7rem; display:flex; align-items:center; gap:.5rem;
}
.sg-step .n {
    display:inline-flex; align-items:center; justify-content:center;
    width:26px; height:26px; border-radius:8px; font-size:.85rem;
    background: linear-gradient(135deg,#8b5cf6,#ec4899); color:#fff;
}

.sg-preview { text-align:center; }
.sg-preview img {
    width:100%; height:300px; object-fit:cover;
    border-radius:16px; border:1px solid rgba(255,255,255,0.14);
    box-shadow: 0 18px 44px rgba(0,0,0,0.35);
}
.sg-cap { color:#cbd5e1; font-size:.85rem; margin-top:.5rem; font-weight:500; }
.sg-result img {
    width:100%; max-width:640px; height:auto; object-fit:contain;
    border-radius:18px; border:1px solid rgba(255,255,255,0.16);
    box-shadow: 0 24px 60px rgba(139,92,246,0.35);
}

/* Gallery */
.sg-gallery-card { text-align:center; margin-bottom:1rem; }
.sg-gallery-card img {
    width:100%; height:180px; object-fit:cover; border-radius:14px;
    border:1px solid rgba(255,255,255,0.12); box-shadow:0 12px 30px rgba(0,0,0,0.3);
}
.sg-gallery-card .d { color:#94a3b8; font-size:.75rem; margin-top:.35rem; }

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.05);
    border: 1.5px dashed rgba(167,139,250,0.5); border-radius: 16px;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color:#a78bfa; background: rgba(167,139,250,0.08);
}
.stFileUploader label, .stTextInput label { color:#e5e7eb !important; font-weight:500; }

.stButton > button, .stDownloadButton > button {
    width:100%;
    background: linear-gradient(90deg,#8b5cf6,#ec4899);
    color:#fff; border:none; border-radius:12px;
    padding:.7rem 1rem; font-weight:600; transition: all .15s ease;
    box-shadow:0 12px 26px rgba(139,92,246,.38);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px); filter: brightness(1.05);
    box-shadow:0 16px 34px rgba(236,72,153,.48);
}

.stAlert { border-radius:14px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,11,46,0.95), rgba(36,20,88,0.95));
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] img { border-radius:12px; }
.sg-side-title { font-family:'Sora',sans-serif; font-weight:700; font-size:1.15rem; color:#f1f5f9; }
.sg-op { text-align:center; font-size:2.4rem; color:#f5d0fe; font-weight:700; margin-top:110px; }
</style>
"""
st.markdown(_THEME_CSS, unsafe_allow_html=True)


def img_to_uri(pil_img):
    buf = BytesIO()
    pil_img.convert("RGB").save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def preview_card(pil_img, caption):
    st.markdown(
        f'<div class="sg-preview"><img src="{img_to_uri(pil_img)}"/>'
        f'<div class="sg-cap">{caption}</div></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="sg-hero">
        <div class="sg-logo">🎨</div>
        <h1 class="sg-title">StyleGenix Studio</h1>
        <p class="sg-sub">Blend a <b>content</b> photo with a <b>style</b> image to create AI artwork.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar — user + inspiration + logout
# ---------------------------------------------------------------------------
with st.sidebar:
    email = st.session_state.get("email", "Artist")
    st.markdown(f'<p class="sg-side-title">👋 {email}</p>', unsafe_allow_html=True)
    st.image(image="./assets/speed-brush.gif")
    st.markdown('<p class="sg-side-title">Some Inspiration 🎨</p>', unsafe_allow_html=True)
    st.caption("A few pieces created with StyleGenix.")

    for c, a in [("content1.jpg", "art1.png"), ("content2.jpg", "art2.png"),
                 ("content3.jpg", "art3.png"), ("content4.jpg", "art4.png")]:
        col1, col2 = st.columns(2)
        with col1:
            st.image(image=f"./assets/{c}")
        with col2:
            st.image(image=f"./assets/{a}")

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        logout()

# ---------------------------------------------------------------------------
# Upload section
# ---------------------------------------------------------------------------
st.markdown('<div class="sg-step"><span class="n">1</span> Upload your images</div>', unsafe_allow_html=True)

col1, col_op, col2 = st.columns([5, 1, 5])
content_file = None
style_file = None

with col1:
    content_file = st.file_uploader("Content image (PNG / JPG)", type=['png', 'jpg', 'jpeg'])
    if content_file is not None:
        preview_card(Image.open(content_file), "Content")

with col_op:
    st.markdown('<div class="sg-op">+</div>', unsafe_allow_html=True)

with col2:
    style_file = st.file_uploader("Style image (PNG / JPG)", type=['png', 'jpg', 'jpeg'])
    if style_file is not None:
        preview_card(Image.open(style_file), "Style")

qcol1, qcol2 = st.columns([2, 3])
with qcol1:
    quality = st.select_slider(
        "🎚️ Output quality",
        options=["Fast", "Balanced", "High"],
        value="High",
        help="Higher quality keeps more detail but takes a little longer.",
    )
QUALITY_DIM = {"Fast": 640, "Balanced": 1024, "High": 1400}
max_dim = QUALITY_DIM[quality]

st.info('Tip: use a **painting / artwork** as the Style image for the best results. '
        'The first run warms up the model; after that it is fast. '
        'Every result is saved to your account.')

# ---------------------------------------------------------------------------
# Result section
# ---------------------------------------------------------------------------
if content_file is not None and style_file is not None:
    st.markdown('<div class="sg-step"><span class="n">2</span> Your artwork</div>', unsafe_allow_html=True)

    content_bytes = content_file.getvalue()
    style_bytes = style_file.getvalue()

    with st.spinner("🎨 Styling your image... (first run warms up the model)"):
        styled_image = stylize(content_bytes, style_bytes, max_dim)

    result_img = Image.fromarray((styled_image * 255).astype(np.uint8))

    # Save to Firebase once per unique (content, style, quality) combination
    pair_key = hashlib.md5(content_bytes + style_bytes + str(max_dim).encode()).hexdigest()
    if st.session_state.get("last_saved") != pair_key:
        ok, err = save_creation(
            Image.open(BytesIO(content_bytes)),
            Image.open(BytesIO(style_bytes)),
            result_img,
        )
        if ok:
            st.session_state["last_saved"] = pair_key
            st.balloons()
            st.toast("Saved to your gallery ✅")
        elif err:
            st.caption(f"(Could not save to Firebase: {err})")

    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        st.markdown(
            f'<div class="sg-result" style="text-align:center;"><img src="{img_to_uri(result_img)}"/></div>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

        buffered = BytesIO()
        result_img.save(buffered, format="JPEG", quality=95)
        st.download_button(
            label="⬇️  Download artwork",
            data=buffered.getvalue(),
            file_name="stylegenix_output.jpg",
            mime="image/jpeg",
        )

# ---------------------------------------------------------------------------
# My Creations gallery (from Firebase)
# ---------------------------------------------------------------------------
st.markdown('<div class="sg-step">🖼️ My Creations</div>', unsafe_allow_html=True)
creations = load_creations()
if not creations:
    st.caption("No saved creations yet — style an image and it will appear here.")
else:
    st.caption(f"{len(creations)} saved artwork(s) in your account.")
    cols = st.columns(4)
    for i, item in enumerate(creations):
        with cols[i % 4]:
            st.markdown(
                f'<div class="sg-gallery-card">'
                f'<img src="data:image/jpeg;base64,{item.get("result", "")}"/>'
                f'</div>',
                unsafe_allow_html=True,
            )
