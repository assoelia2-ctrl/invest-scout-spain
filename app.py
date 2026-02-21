import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain: KI-Immobilien-Analyst")

# Key-Logik
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    try:
        # FORCE: Wir sagen der Bibliothek explizit, welche API-Version sie nutzen soll
        os.environ["GOOGLE_API_USE_MTLS"] = "never"
        genai.configure(api_key=api_key)
        
        # Wir nutzen das stabilste Modell
        model = genai.GenerativeModel('gemini-1.5-flash')

        col1, col2 = st.columns([1, 1])
        with col1:
            st.header("Input & Analyse")
            uploaded_file = st.file_uploader("Bild hochladen...", type=["jpg", "jpeg", "png"])
            user_query = st.text_area("Details zum Investment:", placeholder="Z.B. Suche Haus in Malaga...")
            analyze_button = st.button("🚀 Strategie-Check starten")

        with col2:
            st.header("Ergebnis")
            if analyze_button:
                with st.spinner("KI analysiert..."):
                    inputs = []
                    if uploaded_file:
                        inputs.append(Image.open(uploaded_file))
                    inputs.append(user_query if user_query else "Analysiere dieses Objekt.")
                    
                    response = model.generate_content(inputs)
                    st.markdown(response.text)
                        
    except Exception as e:
        st.error(f"Fehler: {e}")
else:
    st.info("Bitte API Key eingeben.")
