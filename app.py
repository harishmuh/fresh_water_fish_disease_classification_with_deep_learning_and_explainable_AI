import streamlit as st

from config import PAGE_CONFIG
from image_utils import (
    create_overlay,
    load_and_preprocess_image,
    read_original_image,
)
from model_utils import (
    load_model,
    make_gradcam_heatmap,
    predict_image,
)
from ui import (
    inject_css,
    render_about_result,
    render_disclaimer,
    render_header,
    render_image_input,
    render_model_explanation,
    render_prediction,
    render_references,
    render_sidebar,
)


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(**PAGE_CONFIG)


# ============================================================
# Application styling and navigation
# ============================================================

inject_css()
render_sidebar()
render_header()


# ============================================================
# Image input
# ============================================================

image_source, uploaded = render_image_input()


# ============================================================
# Main prediction workflow
# ============================================================

if image_source is not None:

    try:
        model = load_model()

        original_image = read_original_image(
            image_source,
            uploaded=uploaded,
        )

        img_array = load_and_preprocess_image(
            image_source,
            uploaded=uploaded,
        )

        result = predict_image(
            model,
            img_array,
        )

        predicted_label = result["label"]
        confidence = result["confidence"]
        prediction = result["probabilities"]

        heatmap = make_gradcam_heatmap(
            img_array=img_array,
            model=model,
            backbone_name="resnet50",
            last_conv_layer_name="conv5_block3_out",
        )

        overlay = create_overlay(
            original_image,
            heatmap,
        )

        render_model_explanation(
            original_image,
            overlay,
        )

        render_prediction(
            predicted_label,
            confidence,
            prediction,
        )

        render_about_result(
            predicted_label,
        )

        render_references()
        render_disclaimer()

    except Exception as error:
        st.error(
            "The application could not process this image."
        )
        st.exception(error)
