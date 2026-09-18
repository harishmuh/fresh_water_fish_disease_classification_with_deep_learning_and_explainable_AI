import streamlit as st
import textwrap

from config import (
    CLASS_NAMES,
    LOGO_PATH,
    SAMPLE_DIR,
    SUPPORTED_IMAGE_TYPES,
)
from disease_info import DISEASE_INFORMATION, FULL_REFERENCES


def inject_css():
    """Apply FishScan7 visual styling."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background: #f7f9fc;
            border-right: 1px solid #e2e8f0;
        }

        section[data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1.25rem 2rem 1.25rem;
        }

        .sidebar-divider {
            height: 1px;
            background: #dfe6ee;
            margin: 0.7rem 0 1rem 0;
        }

        .sidebar-section {
            color: #263b53;
            font-size: 0.98rem;
            font-weight: 750;
            margin: 0.9rem 0 0.35rem 0;
        }

        .sidebar-value {
            color: #34495e;
            font-size: 0.82rem;
            line-height: 1.45;
            margin-bottom: 0.45rem;
        }

        .intended-use {
            color: #34495e;
            font-size: 0.8rem;
            line-height: 1.5;
        }

        .intended-use ul {
            margin: 0.35rem 0 0.6rem 1.05rem;
            padding: 0;
        }

        .intended-use li {
            margin: 0.15rem 0;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 4.8rem;
            padding-bottom: 2.5rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        div[data-testid="stAppDeployButton"] {
            display: none;
        }

        .main-title {
            color: #183b66;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.05;
            margin: 0.1rem 0 0.15rem 0;
        }

        .main-subtitle {
            color: #718096;
            font-size: 0.84rem;
            line-height: 1.35;
            margin-bottom: 1rem;
        }

        .header-rule {
            height: 1px;
            background: #e7edf4;
            margin: 0 0 1.1rem 0;
        }

        .section-label {
            color: #183b66;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.45rem;
        }

        .soft-card {
            background: #f7f9fc;
            border: 1px solid #e6ebf2;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .result-card {
            background: #f7fbff;
            border: 1px solid #dceaf7;
            border-radius: 12px;
            padding: 1.15rem 1.25rem;
            margin: 0.25rem 0 1rem 0;
        }

        .result-label {
            color: #718096;
            font-size: 0.78rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.07em;
        }

        .result-name {
            color: #183b66;
            font-size: 1.35rem;
            font-weight: 750;
            line-height: 1.25;
            margin-top: 0.25rem;
        }

        .result-confidence {
            color: #2276c9;
            font-size: 1.85rem;
            font-weight: 750;
            margin-top: 0.25rem;
        }

        .small-note {
            color: #718096;
            font-size: 0.78rem;
            line-height: 1.45;
        }

        .prob-row {
            margin: 0.72rem 0 0.85rem 0;
        }

        .prob-head {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            font-size: 0.84rem;
            color: #263b53;
            margin-bottom: 0.28rem;
        }

        .prob-value {
            color: #52657a;
            font-variant-numeric: tabular-nums;
            white-space: nowrap;
        }

        .prob-track {
            width: 100%;
            height: 7px;
            background: #e9eef4;
            border-radius: 99px;
            overflow: hidden;
        }

        .prob-fill {
            height: 100%;
            background: #2b83d5;
            border-radius: 99px;
        }

        .image-title {
            color: #183b66;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .disclaimer {
            background: #fff9df;
            border: 1px solid #f1e3a5;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            color: #6d5a13;
            font-size: 0.79rem;
            line-height: 1.45;
            margin-top: 1.1rem;
        }

        div[data-testid="stFileUploader"] {
            background: white;
            border: 1px solid #dfe6ee;
            border-radius: 10px;
            padding: 0.35rem;
        }

        div[data-baseweb="select"] > div {
            border-radius: 9px;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.55rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the FishScan7 sidebar."""
    with st.sidebar:
        if LOGO_PATH.is_file():
            st.image(
                str(LOGO_PATH),
                width=190,
            )
        else:
            st.markdown(
                '<div class="sidebar-section">FishScan7</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="sidebar-divider"></div>

            <div class="sidebar-section">🗄️ Dataset</div>
            <div class="sidebar-value">
                Freshwater fish disease classification<br>
                7 dataset categories
            </div>

            <div class="sidebar-section">🧠 AI Model</div>
            <div class="sidebar-value">ResNet50</div>

            <div class="sidebar-section">🎯 Prediction Task</div>
            <div class="sidebar-value">
                Multi-label fish disease classification
            </div>

            <div class="sidebar-section">🔎 Explainability</div>
            <div class="sidebar-value">Grad CAM</div>

            <div class="sidebar-divider"></div>

            <div class="sidebar-section">Intended Use</div>
            <div class="intended-use">
                FishScan7 is still under development. The app is intended for:
                <ul>
                    <li>Research</li>
                    <li>AI Demonstration</li>
                    <li>Education</li>
                </ul>
                Not intended for fish disease clinical diagnosis or to replace
                professional veterinary judgement.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_header():
    """Render the main application header."""
    st.markdown(
        """
        <div class="main-title">FishScan7</div>
        <div class="main-subtitle">
            Freshwater Fish Disease Classification using ResNet50
        </div>
        <div class="header-rule"></div>
        """,
        unsafe_allow_html=True,
    )


def render_image_input():
    """Render sample or upload input and return source plus upload flag."""
    st.markdown(
        '<div class="section-label">Image input</div>',
        unsafe_allow_html=True,
    )

    input_mode = st.radio(
        "Select image source",
        ["Use a sample image", "Upload an image"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if input_mode == "Upload an image":
        st.markdown(
            '<div class="soft-card">',
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Upload a fish image",
            type=SUPPORTED_IMAGE_TYPES,
            label_visibility="visible",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.info(
            "⚠️ Fish images only. FishScan7 was developed for freshwater fish images represented by the seven dataset categories."
        )

        if uploaded_file is None:
            return None, False

        return uploaded_file.getvalue(), True

    sample_paths = []

    if SAMPLE_DIR.is_dir():
        valid_extensions = {
            ".jpg", ".jpeg", ".png", ".bmp", ".webp"
        }

        for path in sorted(SAMPLE_DIR.rglob("*")):
            if path.is_file() and path.suffix.lower() in valid_extensions:
                sample_paths.append(path)

    if not sample_paths:
        st.error(f"No sample images were found in {SAMPLE_DIR}")
        return None, False

    sample_labels = [
        str(path.relative_to(SAMPLE_DIR))
        for path in sample_paths
    ]

    selected_label = st.selectbox(
        "Choose a sample image",
        sample_labels,
    )

    return SAMPLE_DIR / selected_label, False


def render_model_explanation(original_image, overlay):
    """Render original image and Grad CAM explanation."""
    st.markdown(
        '<div class="section-label">Model explanation</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(
        [0.75, 0.75],
        gap="large",
    )

    with col1:
        st.markdown(
            '<div class="image-title">Original image</div>',
            unsafe_allow_html=True,
        )
        st.image(
            original_image,
            width=280,
        )

    with col2:
        st.markdown(
            '<div class="image-title">Grad CAM explanation</div>',
            unsafe_allow_html=True,
        )
        st.image(
            overlay,
            width=280,
        )
        st.markdown(
            """
            <div class="small-note">
                Warm regions indicate stronger model activation.
                Cool regions indicate weaker activation.
                Grad CAM highlights image regions that contributed
                strongly to the model prediction.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_prediction(predicted_label, confidence, prediction):
    """Render predicted class and top five probabilities."""
    st.markdown(
        '<div class="section-label" style="margin-top:1.1rem;">Prediction</div>',
        unsafe_allow_html=True,
    )

    result_col, probability_col = st.columns(
        [0.85, 1.5],
        gap="large",
    )

    with result_col:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Predicted class</div>
                <div class="result-name">{predicted_label}</div>
                <div class="result-label" style="margin-top:0.8rem;">
                    Model confidence
                </div>
                <div class="result-confidence">
                    {confidence * 100:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="small-note">
                The confidence value is the model's predicted probability
                for the selected class.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with probability_col:
        from model_utils import probability_rows

        st.markdown(
            '<div class="image-title">Top 5 class probabilities</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            probability_rows(prediction),
            unsafe_allow_html=True,
        )


def render_about_result(predicted_label):
    """Render the scientific information for the predicted category."""
    info = DISEASE_INFORMATION[predicted_label]

    symptoms_html = "".join(
        f"<li>{symptom}</li>"
        for symptom in info["symptoms"]
    )

    about_html = f"""
<div class="section-label" style="margin-top:1.15rem;">ABOUT THIS RESULT</div>

<div class="soft-card">
    <div class="image-title">{info["display_name"]}</div>

    <div style="color:#263b53;font-size:0.84rem;font-weight:700;
                margin-top:0.75rem;margin-bottom:0.2rem;">
        What is it?
    </div>
    <div style="color:#34495e;line-height:1.55;font-size:0.88rem;">
        {info["what_is_it"]}
    </div>

    <div style="color:#263b53;font-size:0.84rem;font-weight:700;
                margin-top:0.75rem;margin-bottom:0.2rem;">
        Symptoms
    </div>
    <ul style="color:#34495e;line-height:1.45;font-size:0.86rem;
               margin-top:0.2rem;margin-bottom:0.35rem;padding-left:1.2rem;">
        {symptoms_html}
    </ul>

    <div style="color:#263b53;font-size:0.84rem;font-weight:700;
                margin-top:0.65rem;margin-bottom:0.2rem;">
        Potential treatment
    </div>
    <div style="color:#34495e;line-height:1.55;font-size:0.88rem;">
        {info["treatment"]}
    </div>

    <div class="small-note" style="margin-top:0.7rem;">
        Reference: {info["reference"]}
    </div>
</div>
"""

    # st.html bypasses Markdown parsing, which prevents the HTML from
    # being displayed as a code block.
    st.html(about_html)


def render_references():
    """Render the complete reference list."""
    with st.expander("References"):
        st.markdown(FULL_REFERENCES)


def render_disclaimer():
    """Render the research prototype disclaimer."""
    st.markdown(
        """
        <div class="disclaimer">
            <strong>Disclaimer:</strong>
            This application is a research prototype and intended for research, educational, and demonstration purposes only. 
            Predictions represent image classifications within seven predefined dataset categories and do not confirm a disease, pathogen, or veterinary diagnosis. 
            Treatment information is general and should not be used as a treatment instruction.
        </div>
        """,
        unsafe_allow_html=True,
    )
