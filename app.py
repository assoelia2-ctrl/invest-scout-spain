import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfiguration der Seite
st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain: KI-Immobilien-Analyst")

# API Key Logik (aus Secrets oder Seitenleiste)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # WICHTIG: Hier nutzen wir den stabilen Modell-Namen ohne v1beta-Pfad
        model = genai.GenerativeModel('gemini-1.5-flash')

        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("Input & Analyse")
            uploaded_file = st.file_uploader("Bild der Immobilie hochladen...", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Objekt Scan", use_container_width=True)
            
            user_query = st.text_area("Zusätzliche Infos (Budget, Ort, Strategie):", 
                                     placeholder="Z.B. Suche Haus in Malaga für 300.000€ zum Kauf")
            
            analyze_button = st.button("🚀 Strategie-Check starten")

        with col2:
            st.header("Ergebnis: Strategisches Exposé")
            if analyze_button:
                if not uploaded_file and not user_query:
                    st.warning("Bitte lade ein Bild hoch oder gib eine Beschreibung ein.")
                else:
                    with st.spinner("KI analysiert das Investment..."):
                        # Liste für die Eingabe vorbereiten
                        inputs = []
                        if uploaded_file:
                            inputs.append(image)
                        if user_query:
                            inputs.append(user_query)
                        else:
                            inputs.append("Analysiere dieses Objekt auf seine Eignung als Investment in Spanien.")
                        
                        response = model.generate_content(inputs)
                        st.markdown(response.text)
                        
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
        st.info("Tipp: Überprüfe, ob dein API Key noch gültig ist.")
else:
    st.info("Bitte hinterlege den API Key in den Streamlit Secrets oder gib ihn in der Seitenleiste ein.")
