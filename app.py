import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Invest-Scout Spain 2026", layout="wide")
st.title("🏠 Invest-Scout Spain")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        # Dieser Befehl erzwingt die Nutzung der stabilen v1 API
        genai.configure(api_key=api_key, transport='rest') 
        
        # Wir nutzen den absolut sichersten Namen
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png"])
        user_query = st.text_area("Details")
        
        if st.button("🚀 Analyse starten"):
            with st.spinner("Analysiere..."):
                content = []
                if uploaded_file:
                    content.append(Image.open(uploaded_file))
                content.append(user_query if user_query else "Analysiere dieses Investment.")
                
                response = model.generate_content(content)
                st.write(response.text)
    except Exception as e:
        st.error(f"Fehler: {e}")
