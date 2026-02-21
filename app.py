import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfiguration der Seite
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain: KI-Immobilien-Analyst")

# 2. API Key Logik (aus Secrets oder Seitenleiste)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    try:
        # Verbindung konfigurieren
        genai.configure(api_key=api_key)
        
        # DAS IST DER FIX: Wir nutzen die sicherste Modell-Bezeichnung
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("Input & Analyse")
            uploaded_file = st.file_uploader("Bild der Immobilie hochladen...", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Objekt Scan", use_container_width=True)
            
            user_query = st.text_area("Details (Z.B. Budget 300k, Malaga, Fokus auf Rendite):")
            analyze_button = st.button("🚀 Strategie-Check starten")

        with col2:
            st.header("Ergebnis: Strategisches Exposé")
            if analyze_button:
                if not uploaded_file and not user_query:
                    st.warning("Bitte gib Daten ein.")
                else:
                    with st.spinner("KI analysiert..."):
                        # Input-Liste sauber aufbauen
                        content_parts = []
                        if uploaded_file:
                            content_parts.append(image)
                        if user_query:
                            content_parts.append(user_query)
                        else:
                            content_parts.append("Analysiere diese Immobilie in Spanien.")
                        
                        # Generierung starten
                        response = model.generate_content(content_parts)
                        st.markdown(response.text)
                        
    except Exception as e:
        st.error(f"Fehler: {e}")
        st.info("Sollte der 404-Fehler bleiben, könnte dein API-Key in einer Region ohne Zugriff auf Flash liegen (eher selten).")
else:
    st.info("Bitte API Key eingeben.")
