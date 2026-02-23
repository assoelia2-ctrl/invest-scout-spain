import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

# 1. Seite stabilisieren
st.set_page_config(page_title="Málaga Invest: Reset", layout="wide")

# Speicher für den Text fest anlegen
if 'ergebnis_text' not in st.session_state:
    st.session_state['ergebnis_text'] = ""

st.title("🛡️ Invest-Scout: Stabiler Modus")

# 2. Upload-Bereich mit festem Key (wichtig für die Stabilität!)
datei = st.file_uploader("Bild oder Screenshot auswählen:", type=["jpg", "png", "jpeg"], key="uploader_v2")

if datei:
    img = Image.open(datei)
    st.image(img, caption="Datei bereit", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        try:
            # Direkte Texterkennung
            ergebnis = pytesseract.image_to_string(img, lang='deu+spa')
            st.session_state['ergebnis_text'] = ergebnis
            st.success("Analyse abgeschlossen!")
        except Exception as e:
            st.error(f"Fehler: {e}")

# 3. Anzeige der Ergebnisse (Nur wenn Analyse erfolgt ist)
if st.session_state['ergebnis_text']:
    st.divider()
    
    # Karte zur Übersicht
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Recherche-Link (Sicherer als ein interaktiver Chat)
    st.markdown("### [🔍 Dubletten-Check bei Google](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    with st.expander("Gelesene Daten anzeigen"):
        st.write(st.session_state['ergebnis_text'])
