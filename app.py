import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfiguration
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain: KI-Immobilien-Analyst")

# API Key Logik (Secrets bevorzugt)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("Input & Analyse")
            uploaded_file = st.file_uploader("Bild der Immobilie hochladen...", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Objekt Scan", use_container_width=True)
            
            user_query = st.text_area("Zusätzliche Infos (Budget, Ort, Strategie):", 
                                     placeholder="Z.B. Budget 300k, Malaga, Fokus auf Rendite...")
            
            analyze_button = st.button("🚀 Strategie-Check starten")

        with col2:
            st.header("Ergebnis: Strategisches Exposé")
            if analyze_button:
                with st.spinner("KI analysiert das Investment..."):
                    inputs = []
                    if uploaded_file:
                        inputs.append(image)
                    inputs.append(user_query if user_query else "Führe eine Immobilienanalyse für dieses Objekt durch.")
                    
                    response = model.generate_content(inputs)
                    st.markdown(response.text)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
else:
    st.info("Bitte hinterlege den API Key in den Streamlit Secrets oder gib ihn in der Seitenleiste ein.")
