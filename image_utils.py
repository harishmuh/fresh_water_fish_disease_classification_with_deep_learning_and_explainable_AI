import io
import os

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from tensorflow.keras.applications.resnet50 import (
    preprocess_input as resnet_preprocess,
)

from config import IMAGE_SIZE, SAMPLE_DIR


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def get_sample_images():
    """Return all supported sample image paths."""
    if not SAMPLE_DIR.is_dir():
        return []

    paths = []

    for root, _, files in os.walk(SAMPLE_DIR):
        for filename in sorted(files):
            extension = os.path.splitext(filename)[1].lower()
            if extension in VALID_EXTENSIONS:
                paths.append(os.path.join(root, filename))

    return sorted(paths)


def load_and_preprocess_image(source, uploaded=False):
    """Load an image and apply the same ResNet50 preprocessing used by the notebook."""

    if uploaded:
        image = tf.io.decode_image(
            source,
            channels=3,
            expand_animations=False,
        )
    else:
        image = tf.io.read_file(
            str(source)
        )

        image = tf.image.decode_image(
            image,
            channels=3,
            expand_animations=False,
        )

    image = tf.image.resize(
        image,
        (IMAGE_SIZE, IMAGE_SIZE),
    )

    image = tf.cast(
        image,
        tf.float32,
    )

    image = tf.expand_dims(
        image,
        axis=0,
    )

    return resnet_preprocess(image)


def read_original_image(source, uploaded=False):
    """Return the original image as a PIL RGB image."""
    if uploaded:
        return Image.open(io.BytesIO(source)).convert("RGB")

    return Image.open(source).convert("RGB")


def create_overlay(original_image, heatmap, alpha=0.4):
    """Overlay a Grad CAM heatmap on the original image."""
    image = np.asarray(original_image).copy()

    heatmap = cv2.resize(
        heatmap,
        (image.shape[1], image.shape[0]),
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET,
    )

    heatmap = cv2.cvtColor(
        heatmap,
        cv2.COLOR_BGR2RGB,
    )

    return cv2.addWeighted(
        image,
        1 - alpha,
        heatmap,
        alpha,
        0,
    )
