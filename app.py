import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(page_title="AI Image Generator Bridge", page_icon="🎨", layout="centered")
st.title("🎨 AI Image Generator Web App")
st.info("🔗 **Backend Notebook** must be active: [csabafarago/image-generator-backend](https://www.kaggle.com/code/csabafarago/image-generator-backend)")

prompt = st.text_area(
    "Describe the image to generate:", 
    value="A majestic dragon flying over a glowing futuristic city, cinematic lighting, 8k",
    height=100
)

if st.button("🚀 Generate Image", type="primary", use_container_width=True):
    if not prompt:
        st.warning(" Please enter a prompt!")
    else:
        with st.spinner(" Connecting to Colab GPU and generating image..."):
            try:
                # Header required by ngrok free tier to skip warning page
                headers = {"ngrok-skip-browser-warning": "true"}
                params = {"prompt": prompt}
                
                # API request to Colab
                response = requests.get(
                    "https://abreast-calm-refining.ngrok-free.dev/generate",
                    params=params, 
                    headers=headers, 
                    timeout=90
                )
                
                if response.status_code == 200:
                    # Receive image from bytes and display
                    image = Image.open(BytesIO(response.content))
                    
                    st.success(" Image generated successfully!")
                    st.image(image, caption=f"Generated: '{prompt}'", use_container_width=True)
                    
                    # Download button
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    st.download_button(
                        label="💾 Download Image (PNG)",
                        data=img_byte_arr.getvalue(),
                        file_name="ai_generated_image.png",
                        mime="image/png"
                    )
                else:
                    st.error(f" Server error occurred! Status code: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.Timeout:
                st.error(" Request timed out! Colab server did not respond in time.")
            except Exception as e:
                st.error(f" Failed to connect to Colab backend: {e}")
