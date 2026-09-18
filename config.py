from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent

# Paths
MODEL_PATH = BASE_DIR / "model" / "resnet50_fish_disease.keras"
SAMPLE_DIR = BASE_DIR / "images" / "samples"
LOGO_PATH = BASE_DIR / "assets" / "logo" / "fishscan7_logo.png"

# Model configuration
IMAGE_SIZE = 224

CLASS_NAMES = [
    "Bacterial Red disease",
    "Bacterial diseases - Aeromoniasis",
    "Bacterial gill disease",
    "Fungal diseases Saprolegniasis",
    "Healthy Fish",
    "Parasitic diseases",
    "Viral diseases White tail disease",
]

# Streamlit configuration
PAGE_CONFIG = {
    "page_title": "FishScan7",
    "page_icon": "🐟",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

SUPPORTED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
    "bmp",
    "webp",
]
