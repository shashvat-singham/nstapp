import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_model(model_path):
    """Load the TF-Hub stylization model once and cache it across reruns.

    Without caching the model was reloaded on every single request, which
    was the main reason styling felt slow.
    """
    return hub.load(model_path)


def transfer_style(content_image, style_image, model_path, max_dim=720):

    """
    :param content_image: content image as numpy array
    :param style_image: style image as numpy array
    :param model_path: path to the downloaded pre-trained model.
    :param max_dim: longest side the content image is scaled to (speed).

    The 'model' directory already contains the downloaded pre-trained model, but
    you can also download the pre-trained model from the below TF HUB link:
    https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2

    :return: A Styled image as 3D numpy array.

    """

    # --------------------------------------------------------------
    # Downscale the content image so inference is fast. The stylization
    # network runs in a fraction of the time on smaller inputs and the
    # perceived quality stays high.
    # --------------------------------------------------------------
    h, w = content_image.shape[:2]
    longest = max(h, w)
    if longest > max_dim:
        scale = max_dim / float(longest)
        content_image = cv2.resize(
            content_image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
        )
        content_image = np.array(content_image)

    # --------------------------------------------------------------

    # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.

    # The style network was trained on ~256px style images.
    style_image = tf.image.resize(style_image, (256, 256))

    # Load (cached) model and stylize.
    hub_module = load_model(model_path)
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]

    # reshape the stylized image
    stylized_image = np.array(stylized_image)
    stylized_image = stylized_image.reshape(
        stylized_image.shape[1], stylized_image.shape[2], stylized_image.shape[3])

    return stylized_image
