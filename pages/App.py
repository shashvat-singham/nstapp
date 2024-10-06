import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
from twilio.rest import Client  # Import Twilio client
from API import transfer_style

# Twilio credentials
TWILIO_SID = 'ACe9c719bbea6c05333515b931ca9b53b8'
TWILIO_AUTH_TOKEN = 'e496953defb0772342625be72fa054dc'
TWILIO_PHONE_NUMBER = '+12096460609'

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )

# Function to handle logout
def logout():
    if 'user' in st.session_state:
        del st.session_state['user']  # Remove user session
    st.session_state['redirect_to_auth'] = True  # Set a flag for redirect
    st.rerun() # Refresh to apply changes

# Check for redirect to authentication
if 'redirect_to_auth' in st.session_state and st.session_state['redirect_to_auth']:
    st.session_state.clear()  # Clear the session state
    st.session_state['redirect'] = True  # Set redirect flag
    st.rerun()  # Redirect to authentication

# Check if user is logged in
if 'user' not in st.session_state:
    st.warning("Please log in to access this page.")
    st.stop()  # Stop execution if not logged in

# Set page configs
st.set_page_config(page_title="Style-Genix", page_icon="./assets/favicon.png", layout="centered")

# Header Section
title = '<p style="text-align: center;font-size: 50px;font-weight: 350;font-family:Cursive "> StyleGenix </p>'
st.markdown(title, unsafe_allow_html=True)

# Introduction Text
st.markdown(
    "<b> <i> Create Digital Art using Machine Learning ! </i> </b>  &nbsp; We take 2 images — Content Image & Style Image — and blend "
    "them together so that the resulting output image retains the core elements of the content image, but appears to "
    "be “painted” in the style of the style reference image.", unsafe_allow_html=True
)

# Example Image
st.image(image="./assets/nst.png")
st.markdown("</br>", unsafe_allow_html=True)

# Sidebar Section
with st.sidebar:
    st.image(image="./assets/speed-brush.gif")
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown('<p style="font-size: 25px;font-weight: 550;">Some Inspiration 🎨</p>', unsafe_allow_html=True)
    st.markdown('Below are some of the art we created using PixelMix.', unsafe_allow_html=True)

    # Example art images
    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content1.jpg")
    with col2:
        st.image(image="./assets/art1.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content2.jpg")
    with col2:
        st.image(image="./assets/art2.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content3.jpg")
    with col2:
        st.image(image="./assets/art3.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content4.jpg")
    with col2:
        st.image(image="./assets/art4.png")

    # Logout Button
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Logout"):
        logout()  # Call logout function

# Body Section
col1, col2 = st.columns(2)
content_image = None
style_image = None
with col1:
    content_image = st.file_uploader("Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
    if content_image is not None:
        # Display the uploaded content image
        content_img = Image.open(content_image)
        st.image(content_img, caption="Uploaded Content Image", use_column_width=True)
  
with col2:
    style_image = st.file_uploader("Upload Style Image (PNG & JPG images only)", type=['png', 'jpg'])
    if style_image is not None:
        # Display the uploaded style image
        style_img = Image.open(style_image)
        st.image(style_img, caption="Uploaded Style Image", use_column_width=True)

st.markdown("</br>", unsafe_allow_html=True)
st.warning('NOTE: You need at least Intel i3 with 8GB memory for proper functioning of this application. ' +
   'Images greater than (2000x2000) are resized to (1000x1000).')

# Add a phone number input for SMS notification
user_phone_number = st.text_input("Enter your phone number for SMS notification:", placeholder="+1234567890")

if content_image is not None and style_image is not None:
    with st.spinner("Styling Images...will take about 20-30 secs"):
        content_image = Image.open(content_image)
        style_image = Image.open(style_image)

        # Convert PIL Image to numpy array
        content_image = np.array(content_image)
        style_image = np.array(style_image)

        # Path of the pre-trained TF model
        model_path = r"model"

        # Output image
        styled_image = transfer_style(content_image, style_image, model_path)
        if style_image is not None:
            st.balloons()

        col1, col2 = st.columns(2)
        with col1:
            st.image(styled_image)
        with col2:
            st.markdown("</br>", unsafe_allow_html=True)
            st.markdown("<b>Your Image is Ready! Click below to download it.</b>", unsafe_allow_html=True)

            # De-normalize the image
            styled_image = (styled_image * 255).astype(np.uint8)
            img = Image.fromarray(styled_image)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            st.download_button(
                label="Download image",
                data=buffered.getvalue(),
                file_name="output.png",
                mime="image/png"
            )

            # Send SMS notification if a phone number is provided
            if user_phone_number:
                send_sms(user_phone_number, "Your styled image is ready for download!")
