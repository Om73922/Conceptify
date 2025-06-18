import streamlit as st

def get_config():
    """Get configuration from sidebar."""
    config = {
        "background_color": "#FFFFFF",
        "shadow_type": "natural",
        "scene_description": "",
        "num_results": 1,
        "aspect_ratio": "1:1",
        "sync": True
    }

    st.sidebar.header("Configuration")

    # Image Generation Settings
    st.sidebar.subheader("Image Generation")
    config["num_results"] = st.sidebar.slider("Number of Results", 1, 4, 1)
    config["aspect_ratio"] = st.sidebar.selectbox(
        "Aspect Ratio",
        ["1:1", "16:9", "9:16", "4:3", "3:4"]
    )
    config["sync"] = st.sidebar.checkbox("Wait for Results", True)

    return config
