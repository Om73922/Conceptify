import streamlit as st
import os
from dotenv import load_dotenv
from services import (
    get_image,
    generate_hd_image
)
# 🎓
st.set_page_config(
    page_title="Conceptify - Concept visualizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
print("Loading environment variables...")
load_dotenv(verbose=True)  # Add verbose=True to see loading details

# Debug: Print environment variable status
api_key = os.getenv("BRIA_API_KEY")
print(f"API Key present: {bool(api_key)}")
print(f"API Key value: {api_key if api_key else 'Not found'}")
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")

def initialize_session_state():
    """Initialize session state variables."""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv('BRIA_API_KEY')
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'pending_urls' not in st.session_state:
        st.session_state.pending_urls = []
    if 'edited_image' not in st.session_state:
        st.session_state.edited_image = None
    if 'original_prompt' not in st.session_state:
        st.session_state.original_prompt = ""
    if 'enhanced_prompt' not in st.session_state:
        st.session_state.enhanced_prompt = None


def main():
    st.title("Conceptify - Concept Visualizer")
    initialize_session_state()

    # Sidebar for API key
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter your API key:", value=st.session_state.api_key if st.session_state.api_key else "", type="password")
        if api_key:
            st.session_state.api_key = api_key

    # Main tabs
    tabs = st.tabs([
        "🎓 Generate Concept Diagram",
    ])

    # Generate Images Tab
    with tabs[0]:
        st.header("Generate Images")

        col1, col2 = st.columns([2, 1])
        with col1:
            # Prompt input
            prompt = st.text_area("Describe your concept (e.g. Photosynthesis, Ancient Rome market)",
                                value="",
                                height=100,
                                key="prompt_input")

        with col2:
            num_images = st.slider("Number of images", 1, 4, 1)
            aspect_ratio = st.selectbox("Aspect ratio", ["1:1", "16:9", "9:16", "4:3", "3:4"])
            enhance_img = st.checkbox("Enhance educational clarity", value=True)

            # Style options
            st.subheader("Style Options")
            style = st.selectbox("Image Style", [
                " Simple diagram", "Detailed labeled diagram", " Realistic scene", " Comic-style"])

            # Add style to prompt
            if style and style != "Realistic":
                prompt = f"{prompt}, in {style.lower()} style"

        # Generate button
        if st.button("🎓 Generate Image", type="primary"):
            if not st.session_state.api_key:
                st.error("Please enter your API key in the sidebar.")
                return

            with st.spinner("🎓 Generating your concept diagram..."):
                try:
                    # Convert aspect ratio to proper format
                    result = generate_hd_image(
                        prompt=st.session_state.enhanced_prompt or prompt,
                        api_key=st.session_state.api_key,
                        num_results=num_images,
                        aspect_ratio=aspect_ratio,  # Already in correct format (e.g. "1:1")
                        sync=True,  # Wait for results
                        enhance_image=enhance_img,
                        medium="art" if style != "Realistic" else "photography",
                        prompt_enhancement=True,
                        content_moderation=False  # Content moderation Diasbled by default
                    )

                    if result:

                        if isinstance(result, dict):
                            if "result_url" in result:
                                st.session_state.edited_image = result["result_url"]
                                st.success("✨ Image generated successfully!")
                            elif "result_urls" in result:
                                st.session_state.edited_image = result["result_urls"][0]
                                st.success("✨ Image generated successfully!")
                            elif "result" in result and isinstance(result["result"], list):
                                for item in result["result"]:
                                    if isinstance(item, dict) and "urls" in item:
                                        st.session_state.edited_image = item["urls"][0]
                                        st.success("✨ Image generated successfully!")
                                        break
                                    elif isinstance(item, list) and len(item) > 0:
                                        st.session_state.edited_image = item[0]
                                        st.success("✨ Image generated successfully!")
                                        break
                        else:
                            st.error("No valid result format found in the API response.")


                        # Debug logging
                        for i in range(num_images):
                            st.write("Url's to Generated Images", result['result'][i]['urls'])

                            with st.spinner('Loading image...'):
                                image_data = get_image(result['result'][i]['urls'])
                            if image_data:
                                st.image(image_data, caption='Downloaded image', use_column_width=True)
                                print("Image displayed successfully in Streamlit.")
                            else:
                                st.warning(f"Could not display image {i + 1}.")
                                print("Image data was None; no image displayed.")

                except Exception as e:
                    st.error(f"Error generating images: {str(e)}")
                    st.write("Full error:", str(e))

if __name__ == "__main__":
    main()
