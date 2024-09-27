import streamlit as st
import pyrebase
# from App import app 
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

# Streamlit app layout
st.set_page_config(page_title="Authentication System", layout="centered")
st.markdown("""
<style>
    body {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        color: #333;
        margin: 20px 0;
    }
    .container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: auto;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        text-align: center;
        display: inline-block;
        font-size: 16px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button:hover {
        background-color: #45a049;
    }
    .link {
        color: #007BFF;
        cursor: pointer;
    }
    .link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

st.title("Authentication System")
st.header("Welcome to StyleGenix")

# Navigation options
option = st.selectbox("Select an option:", ["Sign In", "Register", "Forgot Password"])

if 'user' not in st.session_state:
    with st.form(key='auth_form'):
        if option == "Sign In":
            st.subheader("Sign In")
            email_signin = st.text_input("Email", "")
            password_signin = st.text_input("Password", "", type="password")
            submit_button = st.form_submit_button(label="Sign In")
            if submit_button:
                if sign_in(email_signin, password_signin):
                    st.session_state['redirect'] = True
                    st.rerun()  # Updated method
                else:
                    st.error("Invalid email or password.")

        elif option == "Register":
            st.subheader("Register")
            email_register = st.text_input("Email", "")
            password_register = st.text_input("Password", "", type="password")
            submit_button = st.form_submit_button(label="Register")
            if submit_button:
                if email_register and password_register:  # Basic validation
                    register(email_register, password_register)
                else:
                    st.error("Please fill in both fields.")

        elif option == "Forgot Password":
            st.subheader("Reset Password")
            email_reset = st.text_input("Enter your email", "")
            submit_button = st.form_submit_button(label="Send Reset Email")
            if submit_button:
                if email_reset:  # Basic validation
                    reset_password(email_reset)
                else:
                    st.error("Please enter your email.")

else:
    # If logged in, redirect to App.py
    st.switch_page("pages/App.py")

st.markdown("---")
st.markdown("Made with ❤️ by StyleGenix")
