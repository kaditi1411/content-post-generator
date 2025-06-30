import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Configure page
st.set_page_config(
    page_title="Content Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        color: white;
    }
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1rem 2rem; background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px); border-radius: 10px; margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .user-info {
        color: #64b5f6; font-size: 1rem;
    }
    .main-title {
        text-align: center; font-size: 3.5rem; font-weight: 700;
        margin: 2rem 0; background: linear-gradient(45deg, #64b5f6, #42a5f5, #2196f3);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(33, 150, 243, 0.3);
    }
    .login-container, .post-container {
        max-width: 600px; margin: auto; padding: 2rem; background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 188, 212, 0.2);
    }
    .login-btn, .generate-btn {
        display: flex; justify-content: center; margin: 2rem 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #00bcd4, #0097a7); color: white;
        padding: 0.75rem 2rem; border: none; border-radius: 10px;
        font-size: 1.1rem; font-weight: 600; cursor: pointer;
        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0, 188, 212, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 188, 212, 0.5);
        background: linear-gradient(45deg, #0097a7, #00838f);
    }
</style>
""", unsafe_allow_html=True)

# Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# Login Page
def login_page():
    st.markdown('<h1 class="main-title">Login</h1>', unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(f"{BACKEND_URL}/auth/token", data={
                "username": username,
                "password": password
            }, headers={"Content-Type": "application/x-www-form-urlencoded"})

            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# Post Generator Page
def post_generator_page():
    st.markdown("""
    <div class="header-container">
        <div class="user-info">Logged in as: MECON</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Content Generator</h1>', unsafe_allow_html=True)

    # Select Inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        title = st.selectbox("Title", [
            "Resilience", "Leadership", "Innovation", "Growth Mindset", 
            "Team Building", "Success", "Motivation", "Productivity",
            "Networking", "Career Development"
        ])

    with col2:
        length = st.selectbox("Length", ["Short", "Medium", "Long"])

    with col3:
        language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Hindi", "Urdu"])

    if st.button("Generate Post"):
        try:
            response = requests.post(f"{BACKEND_URL}/generate", json={
                "title": title,
                "length": length,
                "language": language
            }, headers={"Authorization": f"Bearer {st.session_state.token}"})

            if response.status_code == 200:
                post_content = response.json().get("post", "No content generated.")
                st.markdown(f"""
                <div class="post-container">
                    <h3 style="color: #64b5f6; margin-bottom: 1rem;">Generated Content:</h3>
                    <div style="color: white; line-height: 1.6; font-size: 1rem;">{post_content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Error generating post.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Main Logic
if not st.session_state.logged_in:
    login_page()
else:
    post_generator_page()
