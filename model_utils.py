import streamlit as st
import tensorflow as tf
from tensorflow import keras

from config import CLASS_NAMES, MODEL_PATH
from tensorflow.keras.applications.resnet50 import (
    preprocess_input as resnet_preprocess,
)


@st.cache_resource
def load_model():
    """Load the trained FishScan7 ResNet50 model once per Streamlit session."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return keras.models.load_model(
        MODEL_PATH,
        compile=False,
    )


def predict_image(model, img_array):
    """Run model prediction and return structured prediction results."""
    probabilities = model.predict(
        img_array,
        verbose=0,
    )[0]

    pred_index = int(tf.argmax(probabilities).numpy())

    return {
        "index": pred_index,
        "label": CLASS_NAMES[pred_index],
        "confidence": float(probabilities[pred_index]),
        "probabilities": probabilities,
        "image_array": img_array,
    }


def make_gradcam_heatmap(
    img_array,
    model,
    backbone_name="resnet50",
    last_conv_layer_name="conv5_block3_out",
):
    """
    Generate Grad CAM using the same target convolutional layer
    and custom classification head used in the notebook.
    """
    backbone = model.get_layer(backbone_name)

    feature_extractor = tf.keras.Model(
        inputs=backbone.inputs,
        outputs=backbone.get_layer(
            last_conv_layer_name
        ).output,
    )

    head_layers = model.layers[1:]

    with tf.GradientTape() as tape:
        conv_outputs = feature_extractor(
            img_array,
            training=False,
        )

        tape.watch(conv_outputs)
        x = conv_outputs

        for layer in head_layers[:-1]:
            if isinstance(
                layer,
                (
                    tf.keras.layers.BatchNormalization,
                    tf.keras.layers.Dropout,
                ),
            ):
                x = layer(
                    x,
                    training=False,
                )
            else:
                x = layer(x)

        final_dense = head_layers[-1]

        logits = (
            tf.matmul(
                x,
                final_dense.kernel,
            )
            + final_dense.bias
        )

        pred_index = tf.argmax(logits[0])
        loss = logits[:, pred_index]

    grads = tape.gradient(
        loss,
        conv_outputs,
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2),
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1,
    )

    heatmap = tf.maximum(
        heatmap,
        0,
    )

    max_heat = tf.reduce_max(heatmap)

    if float(max_heat.numpy()) > 0:
        heatmap /= max_heat

    return heatmap.numpy()


def probability_rows(prediction, top_n=5):
    """Build HTML for the top-N class probability bars."""
    probability_order = prediction.argsort()[::-1][:top_n]

    html = ""

    for rank, index in enumerate(probability_order):
        label = CLASS_NAMES[index]
        probability = float(prediction[index])
        width = max(probability * 100, 0.15)
        font_weight = "700" if rank == 0 else "500"

        html += f"""
        <div class="prob-row">
            <div class="prob-head">
                <span style="font-weight:{font_weight};">{label}</span>
                <span class="prob-value">{probability * 100:.2f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{width:.3f}%;"></div>
            </div>
        </div>
        """

    return html
