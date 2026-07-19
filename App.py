import streamlit as st
import pyrebase

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="StyleGenix · Sign in",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Theme (inlined so no extra module import is needed on Streamlit Cloud)
# ---------------------------------------------------------------------------
_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stDecoration"] {display: none;}

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

.block-container {
    max-width: 640px;
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

/* ---------- Inputs ---------- */
.stTextInput input, .stTextInput input:focus {
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
.stTextInput label, .stTextInput label p, label p {
    color: #e5e7eb !important; font-weight: 500;
}
.stTextInput input::placeholder { color: #94a3b8; }

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    width: 100%;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    color: #fff; border: none; border-radius: 12px;
    padding: .72rem 1rem; font-weight: 600; font-size: 1rem;
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
    box-shadow: 0 12px 26px rgba(139,92,246,.38);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
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
div[role="radiogroup"] > label > div:first-child { display: none; }
div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    color: #fff; box-shadow: 0 8px 20px rgba(139,92,246,.4);
}

.stAlert { border-radius: 14px; }

.sg-section {
    font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.15rem;
    color: #f1f5f9; margin: .2rem 0 .6rem;
}

.sg-footer {
    text-align: center; color: #94a3b8; font-size: .85rem;
    margin-top: 2.2rem; font-weight: 300;
}
.sg-footer b { color: #c4b5fd; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,11,46,0.9), rgba(36,20,88,0.9));
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ---------- Custom GitHub link (points to the project repo) ---------- */
.sg-gh {
    position: fixed; top: 14px; right: 16px; z-index: 1000;
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: #fff; background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(8px);
    transition: transform .15s ease, background .15s ease;
    text-decoration: none;
}
.sg-gh:hover {
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    transform: translateY(-2px);
}
.sg-gh svg { width: 22px; height: 22px; fill: currentColor; }
</style>
"""
st.markdown(_THEME_CSS, unsafe_allow_html=True)

# Custom GitHub icon -> project repository (neural-style-transfer)
st.markdown(
    """
    <a class="sg-gh" href="https://github.com/shashvat-singham/neural-style-transfer"
       target="_blank" rel="noopener" title="View project on GitHub">
        <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>
    </a>
    """,
    unsafe_allow_html=True,
)

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyDJiQuv0cZ-AiObYbtQHhtTABhLm-Smxrg",
    "authDomain": "stylegenix-b8eed.firebaseapp.com",
    "projectId": "stylegenix-b8eed",
    "storageBucket": "stylegenix-b8eed.appspot.com",
    "messagingSenderId": "835045766386",
    "appId": "1:835045766386:web:3fe54f2c171b1fa303cc6b",
    "measurementId": "G-LX246R50J9",
    "databaseURL": "https://stylegenix-b8eed.firebaseio.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


# Function to handle sign in
def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state['user'] = user['idToken']
        return True
    except Exception as e:
        st.error(f"Error during sign in: {e}")
        return False


# Function to handle registration
def register(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        st.success("Registration successful! Please verify your email.")
    except Exception as e:
        st.error(f"Error during registration: {e}")


# Function to handle password reset
def reset_password(email):
    try:
        auth.send_password_reset_email(email)
        st.success("Password reset email sent!")
    except Exception as e:
        st.error(f"Error sending reset email: {e}")


# If already logged in, go straight to the app
if 'user' in st.session_state:
    st.switch_page("pages/Style_Transfer.py")

# ---------- Hero ----------
st.markdown(
    """
    <div class="sg-hero">
        <div class="sg-logo">🎨</div>
        <h1 class="sg-title">Welcome to StyleGenix</h1>
        <p class="sg-sub">Turn your photos into stunning AI artwork. Sign in to start creating.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Auth options (segmented pills) ----------
option = st.radio(
    "Select an option:",
    ["Sign In", "Register", "Forgot Password"],
    horizontal=True,
    label_visibility="collapsed",
)

with st.form(key='auth_form'):
    if option == "Sign In":
        st.markdown('<div class="sg-section">🔐 Sign In</div>', unsafe_allow_html=True)
        email_signin = st.text_input("Email", "", placeholder="you@example.com")
        password_signin = st.text_input("Password", "", type="password", placeholder="Your password")
        submit_button = st.form_submit_button(label="Sign In →")
        if submit_button:
            if sign_in(email_signin, password_signin):
                st.session_state['redirect'] = True
                st.rerun()
            else:
                st.error("Invalid email or password.")

    elif option == "Register":
        st.markdown('<div class="sg-section">✨ Create your account</div>', unsafe_allow_html=True)
        email_register = st.text_input("Email", "", placeholder="you@example.com")
        password_register = st.text_input("Password", "", type="password", placeholder="Choose a strong password")
        submit_button = st.form_submit_button(label="Register")
        if submit_button:
            if email_register and password_register:  # Basic validation
                register(email_register, password_register)
            else:
                st.error("Please fill in both fields.")

    elif option == "Forgot Password":
        st.markdown('<div class="sg-section">🔑 Reset your password</div>', unsafe_allow_html=True)
        email_reset = st.text_input("Enter your email", "", placeholder="you@example.com")
        submit_button = st.form_submit_button(label="Send Reset Email")
        if submit_button:
            if email_reset:  # Basic validation
                reset_password(email_reset)
            else:
                st.error("Please enter your email.")

st.markdown(
    '<div class="sg-footer">Made with ❤️ by <b>StyleGenix</b> · Neural Style Transfer</div>',
    unsafe_allow_html=True,
)
