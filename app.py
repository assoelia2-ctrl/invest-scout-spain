import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API-Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API-Key fehlt in den Secrets!")

# 2. Analyse-Logik
def analyze_image(img):
    prompt = "Du bist Baugutachter in Andalusien. Analysiere diesen Screenshot auf: 1. Substanz (Risse, Feuchtigkeit), 2. Zufahrt (Asphalt/Schotter), 3. Solar-Potential. Gliedere in RISIKEN, CHANCEN und KOSTEN."
    response = model.generate_content([prompt, img])
    return response.text

# 3. App-Interface
st.set_page_config(page_title="Andalusien Invest Scout")
st.title("☀️ Andalusien Real Estate Master")

uploaded_files = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        st.divider()
        img = Image.open(file)
        st.image(img, width=300)
        
        if st.button(f"🔍 Analyse starten (Bild {i+1})", key=f"btn_{i}"):
            with st.spinner("KI arbeitet..."):
                try:
                    result = analyze_image(img)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Fehler: {e}")
