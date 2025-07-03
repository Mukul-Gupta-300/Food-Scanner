import streamlit as st
from PIL import Image
import base64

# Set page config with favicon
favicon = Image.open("C:/games/coding/nutrition/Diet-Recommendation-System-main/Streamlit_Frontend/logo.jpeg")
st.set_page_config(page_title="Nutridex", page_icon=favicon, layout="wide")

# Function to load and encode the image
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Logo path
logo_path = "C:/games/coding/nutrition/Diet-Recommendation-System-main/Streamlit_Frontend/logo.jpeg"
encoded_logo = get_image_base64(logo_path)

st.markdown("""
<style>
    .main-header {
        background-color: #00A86B;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
    }
    .main-header img {
        width: 80px;
        height: auto;
        margin-right: 20px;
    }
    .main-header h1 {
        color: white;
        font-size: 48px;
        margin: 0;
    }
    .subheader {
        font-size: 24px;
        color: #333;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .fact-box {
        background-color: #e6ffe6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    .fact-box img {
        width: 40px;
        height: auto;
        margin-right: 10px;
    }
    .logo-footer {
        text-align: center;
        margin-top: 30px;
    }
    .logo-footer img {
        width: 100px;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="main-header">
        <img src="data:image/jpeg;base64,{encoded_logo}" alt="Nutridex Logo">
        <h1>Nutridex</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p class='subheader'>Welcome to the Diet Recommendation System of Nutridex</p>", unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <h3>Why Diet Recommendations Matter</h3>
        <p>A personalized diet plan can significantly improve your health, energy levels, and overall well-being. Our system takes into account your unique needs, preferences, and health goals to provide tailored nutrition advice.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h3>Quick Nutrition Facts</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="fact-box">
            <img src="data:image/jpeg;base64,{encoded_logo}" alt="Nutridex Logo">
            <div>
                <strong>Did you know?</strong> Eating a rainbow of colorful fruits and vegetables ensures you get a wide variety of essential nutrients.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="fact-box">
            <img src="data:image/jpeg;base64,{encoded_logo}" alt="Nutridex Logo">
            <div>
                <strong>Hydration Tip:</strong> Drinking water before meals can help control portion sizes and improve digestion.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <h3>How Diet recommendation system of Nutridex Helps You</h3>
        <ul>
            <li>Personalized meal plans based on your age and height</li>
            <li>Personalized meal plans based on your nutrition needs</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("Ready to start your journey to better health? Use the sidebar to explore our recommendation options!")

st.markdown(f"""
    <div class="logo-footer">
        <img src="data:image/jpeg;base64,{encoded_logo}" alt="Nutridex Logo">
        <p>Powered by Nutridex</p>
    </div>
""", unsafe_allow_html=True)