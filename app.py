import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

# 1. Radikaler Reset der Seite
st.set_page_config(page_title="Málaga Invest: Reset", layout="wide")

# Speicher bereinigen
if 'text_speicher' not in st.session_state:
    st.session_state['text_speicher'] = ""

st.title("🛡️ Invest-Scout: Back to Life")

# 2. Einfachster Upload (ohne Schnickschnack)
bild_datei = st.file_uploader("Bild auswählen:", type=["jpg", "png", "jpeg"], key="reset_uploader")

if bild_datei:
    # Bild sofort anzeigen
    img = Image.open(bild_datei)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        try:
            # Nur Texterkennung (OCR)
            ergebnis = pytesseract.image_to_string(img, lang='deu+spa')
            st.session_state['text_speicher'] = ergebnis
            st.success("Erfolg! Analyse abgeschlossen.")
        except Exception as e:
            st.error(f"Fehler: {e}")
            st.info("Prüfe, ob die 'packages.txt' in GitHub vorhanden ist.")

# 3. Wenn Text da ist, zeige Ergebnisse
if st.session_state['text_speicher']:
    st.divider()
    
    # Karte (Málaga Standard)
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Recherche-Link (Sicherer als Chat)
    st.markdown("### [🔍 Dubletten-Check bei Google](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    with st.expander("Gelesene Daten anzeigen"):
        st.write(st.session_state['text_speicher'])
