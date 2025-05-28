import streamlit as st

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
    .influencer-names {
        text-align: center; margin: 1rem 0 2rem 0;
    }
    .influencer-name {
        display: block; color: #64b5f6; font-size: 1.1rem; font-weight: 600;
        margin: 0.3rem 0; transition: all 0.3s ease;
    }
    .influencer-name:hover {
        color: #42a5f5; transform: scale(1.05);
    }
    .generate-btn {
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
    .generated-post {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 10px; padding: 1.5rem; margin-top: 2rem;
        box-shadow: 0 5px 20px rgba(100, 181, 246, 0.1);
    }
    .post-content {
        color: #e3f2fd; line-height: 1.6; font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="user-info">Logged in as: MECON</div>
</div>
""", unsafe_allow_html=True)

# Title and Influencer
st.markdown('<h1 class="main-title">Content Generator</h1>', unsafe_allow_html=True)
st.markdown('<div class="influencer-names"><span class="influencer-name">KHUSHBU_RANI</span></div>', unsafe_allow_html=True)

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

# Post templates
post_templates = {
    "Resilience": {
        "Short": "Hi, my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon ",
        "Medium": "This is for Medium length, Hi, my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon",
        "Long": "This is for Long Length, Hi my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon "
    },
    "Leadership": {
        "Short": "Hi, my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon ",
        "Medium": "This is for Medium length, Hi, my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon",
        "Long": "This is for Long Length, Hi my name is Khushbu Rani, and I am testing my frontend. #internship, #Meccon "
    }
}

# Generate button
if st.button("Generate Post"):
    try:
        selected_template = post_templates.get(title, post_templates["Resilience"])
        post_content = selected_template.get(length, selected_template["Short"])

        # Add language note if not English
        if language != "English":
            post_content = f"[This post would be generated in {language}]\n\n" + post_content

        # Display result
        st.markdown(f"""
        <div class="generated-post">
            <h3 style="color: #64b5f6; margin-bottom: 1rem;">Generated Content:</h3>
            <div class="post-content">{post_content.replace('\n', '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)