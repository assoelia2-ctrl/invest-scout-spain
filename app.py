import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Seite konfigurieren
st.set_page_config(page_title="KI-Agent PRO", layout="wide")

# 2. API Key sicher laden
try:
    # Sucht in den Streamlit Secrets nach GOOGLE_API_KEY
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.sidebar.success("✅ KI-Verbindung aktiv")
except Exception as e:
    st.sidebar.error("❌ API Key fehlt oder falsch")
    st.info("Bitte trage den Key in den Streamlit 'Secrets' ein.")
    st.stop()

# 3. Das Interface
st.title("🤖 Dein KI-Immo-Agent")

user_query = st.text_area("Befehl an den Agenten:", placeholder="Suche Immobilien in...")
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

if st.button("🚀 Agenten beauftragen"):
    if user_query:
        with st.spinner("Agent arbeitet..."):
            try:
                content = [user_query]
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    content.append(img)
                
                response = model.generate_content(content)
                st.markdown("### 📩 Analyse-Ergebnis")
                st.write(response.text)
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")
    else:
        st.warning("Bitte gib einen Text ein.")
