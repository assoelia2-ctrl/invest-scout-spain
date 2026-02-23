import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd

# 1. System-Konfiguration
st.set_page_config(page_title="Málaga Invest: Safe Mode", layout="wide")

# Initialisiere Speicher (Darf niemals gelöscht werden)
if 'extrahierter_text' not in st.session_state:
    st.session_state['extrahierter_text'] = ""

st.title("🛡️ Invest-Scout: Analyse & Recherche")

# 2. ISOLIERTER UPLOAD-BEREICH
# Wir nutzen einen eindeutigen Key, damit der Upload stabil bleibt
datei = st.file_uploader("Bild oder Screenshot hochladen:", 
                         type=["jpg", "png", "jpeg"], 
                         key="immobilien_safe_uploader")

if datei:
    # Bild sofort anzeigen
    img = Image.open(datei)
    st.image(img, caption="Datei geladen", use_container_width=True)
    
    # Analyse-Knopf
    if st.button("🚀 ANALYSE STARTEN", key="start_btn"):
        with st.spinner("Extrahiere Daten..."):
            try:
                # Bild für die Erkennung optimieren
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                # Texterkennung
                text = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['extrahierter_text'] = text
                st.success("Analyse erfolgreich abgeschlossen!")
            except Exception as e:
                st.error(f"Technischer Fehler: {e}")

# 3. INTERAKTIONS-BEREICH (Wird erst nach Analyse eingeblendet)
if st.session_state['extrahierter_text']:
    st.divider()
    
    # Recherche-Optionen
    st.markdown(f"### [🔍 Dubletten-Check bei Google starten](https://www.google.com/search?q=Málaga+Immobilie+Invest)")
    
    # Karte zur Übersicht
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Einfache Fragen zum Dokument
    st.subheader("💬 Schnelle Dokumenten-Abfrage")
    frage = st.text_input("Geben Sie ein Stichwort ein (z.B. Bohrbrunnen):", key="search_query")
    
    if frage:
        if frage.lower() in st.session_state['extrahierter_text'].lower():
            st.success(f"✅ Begriff '{frage}' im Dokument gefunden!")
            # Zeige Kontext an
            t = st.session_state['extrahierter_text']
            pos = t.lower().find(frage.lower())
            st.info(f"...{t[max(0, pos-50):pos+100]}...")
        else:
            st.warning(f"❌ '{frage}' wurde im aktuellen Scan nicht erkannt.")
