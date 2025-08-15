import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")  # Update if needed

# Page config
st.set_page_config(
    page_title="Modesty Fashion Guide Bot",
    page_icon="🧕",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling and background gradient
st.markdown(
    """
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #f0f4ff, #d9e4ff);
        min-height: 100vh;
    }
    /* Title style */
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4B0082;  /* Indigo */
        margin-bottom: 0.5rem;
    }
    /* Subtitle style */
    .subtitle {
        font-size: 1.2rem;
        color: #6A5ACD;  /* SlateBlue */
        margin-bottom: 2rem;
    }
    /* Button style */
    .stButton>button {
        background-color: #4B0082;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #6A5ACD;
        cursor: pointer;
    }
    /* Sidebar header */
    .sidebar .sidebar-content h2 {
        color: #4B0082;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    /* Sidebar paragraphs */
    .sidebar .sidebar-content p {
        font-size: 0.95rem;
        color: #333;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar content with fashion tips and About Me
st.sidebar.markdown("## Modesty Fashion Tips")
st.sidebar.markdown("""
- Choose breathable fabrics like cotton or linen for hot weather.
- Opt for layering to stay warm and modest in cold weather.
- Neutral and pastel colors work well for most occasions.
- Try different hijab styles: turban, draped, or layered for variety.
- Comfort is key: select outfits that allow movement and confidence.
""")

st.sidebar.markdown("---")

st.sidebar.markdown("## About Me")
st.sidebar.markdown("""
Hi! I'm Maria, a passionate modest fashion enthusiast and software developer.  
I created this app to help you find stylish and comfortable modest outfit ideas tailored to your occasion and environment.  
Feel free to reach out or suggest improvements!
**Email:** hameed.maria06@gmail.com 
**LinkedIn:** www.linkedin.com/in/maria-hameed1987
""")

# Initialize session state for inputs if not exist
if "occasion" not in st.session_state:
    st.session_state.occasion = "Wedding"
if "location" not in st.session_state:
    st.session_state.location = ""
if "weather" not in st.session_state:
    st.session_state.weather = "Hot"
if "gender" not in st.session_state:
    st.session_state.gender = "Female"

# Main title and subtitle
st.markdown('<div class="title">Modesty Fashion Guide Bot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Describe your occasion, location, weather, and gender to get a tailored modest outfit suggestion.</div>',
    unsafe_allow_html=True,
)

# Input widgets with session state
occasion = st.selectbox(
    "Select occasion",
    ["Wedding", "Work", "Casual", "Religious Event"],
    index=["Wedding", "Work", "Casual", "Religious Event"].index(st.session_state.occasion),
    key="occasion",
)
location = st.text_input("Enter your city/location", value=st.session_state.location, key="location")
weather = st.selectbox(
    "Select current weather",
    ["Hot", "Cold", "Rainy", "Moderate"],
    index=["Hot", "Cold", "Rainy", "Moderate"].index(st.session_state.weather),
    key="weather",
)
gender = st.selectbox(
    "Select gender",
    ["Female", "Male"],
    index=["Female", "Male"].index(st.session_state.gender),
    key="gender",
)

def generate_outfit_suggestion(occasion, location, weather, gender):
    prompt = f"""
You are a helpful modest fashion assistant. Based on the user's input about occasion, location, weather, and gender, suggest a modest outfit idea. Include fabric types, colors, and hijab styles (if female) or modest styling tips (if male) suitable for the event. Provide styling tips in a friendly tone.

User input:
- Occasion: {occasion}
- Location: {location}
- Weather: {weather}
- Gender: {gender}

Answer:
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# Buttons in two columns: Get Suggestion and Clear
col1, col2 = st.columns([1, 1])

with col1:
    get_suggestion = st.button("Get Outfit Suggestion")

with col2:
    clear_inputs = st.button("Clear")

if get_suggestion:
    if not location.strip():
        st.warning("Please enter your city/location.")
    else:
        with st.spinner("Generating your outfit suggestion..."):
            suggestion = generate_outfit_suggestion(occasion, location, weather, gender)
            st.markdown("### Outfit Suggestion")
            st.write(suggestion)

if clear_inputs:
    st.session_state.occasion = "Wedding"
    st.session_state.location = ""
    st.session_state.weather = "Hot"
    st.session_state.gender = "Female"
    