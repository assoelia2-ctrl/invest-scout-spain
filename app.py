import streamlit as st
import google.generativeai as genai

# 1. API KEY AUS DEN SECRETS LADEN
# Das 'transport=rest' verhindert den gRPC-Fehler aus deinen Logs
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Bitte trage den GEMINI_API_KEY in den Streamlit Secrets ein!")
    st.stop()

st.title("🤖 Málaga Invest-Scout")

# Einfaches Test-Feld
query = st.text_input("Was suchst du?", "Finca in Málaga")
if st.button("Analyse starten"):
    try:
        # Wir erzwingen die Nutzung der stabilen API v1
        response = model.generate_content(query)
        st.write(response.text)
    except Exception as e:
        st.error(f"Fehler: {e}")
        st.info("Falls hier '404' steht, musst du die App löschen und neu erstellen.")
