import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

# 1. Radikaler Reset der Seite
st.set_page_config(page_title="Málaga Invest: Reset", layout="wide")

# Speicher leeren, falls Murks drinsteht
if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = ""

st.title("🛡️ Invest-Scout: Back to Life")

# 2. Upload (Einfachste Version)
uploaded_file = st.file_uploader("Bild auswählen:", type=["jpg", "png", "jpeg"], key="reset_uploader")

if uploaded_file:
    # Bild sofort anzeigen
    img = Image.open(uploaded_file)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        try:
            # Nur Texterkennung ohne Schnickschnack
            text = pytesseract.image_to_string(img, lang='deu+spa')
            st.session_state['doc_text'] = text
            st.success("Erfolg! Daten sind bereit.")
        except Exception as e:
            st.error(f"Technischer Fehler: {e}")

# 3. Wenn Text da ist, zeige Karte und Recherche-Link
if st.session_state['doc_text']:
    st.divider()
    st.subheader("📍 Standort & Recherche")
    
    # Karte (Málaga Standard)
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Die "Kommunikation" lösen wir über einen Button zur Google-Recherche
    # Das ist sicherer als ein Chat-Feld, das die App zum Absturz bringt
    st.markdown(f"### [🔍 Dubletten-Check im Internet](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    with st.expander("Gelesene Daten anzeigen"):
        st.write(st.session_state['doc_text'])
