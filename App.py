import streamlit as st
import pyrebase
from ui import inject_theme, hero, footer

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="StyleGenix · Sign in",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_theme()

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
hero(
    title="Welcome to StyleGenix",
    subtitle="Turn your photos into stunning AI artwork. Sign in to start creating.",
    logo="🎨",
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

footer()
