import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# 1. GRUNDGERÜST (Darf niemals verschoben werden)
st.set_page_config(page_title="Málaga Invest: Ultimate Stability", layout="wide")

# Speicher initialisieren, damit die App nicht abstürzt
if 'text_inhalt' not in st.session_state:
    st.session_state['text_inhalt'] = ""

st.title("🛡️ Invest-Scout: Analyse & Recherche")

# 2. DER DOPPEL-UPLOAD (Bild & Screenshot)
# Durch den festen 'key' bleibt die Datei auch beim Chatten im Speicher
datei = st.file_uploader("Bild oder Screenshot hier hochladen:", 
                         type=["jpg", "png", "jpeg"], 
                         key="immobilien_uploader")

if datei:
    # Sofortige Anzeige des Bildes zur Bestätigung
    img = Image.open(datei)
    st.image(img, caption="Datei erfolgreich geladen", use_container_width=True)
    
    col_anal, col_rech = st.columns(2)
    
    with col_anal:
        if st.button("🚀 ANALYSE STARTEN", key="btn_analyse"):
            with st.spinner("Extrahiere Daten aus Dokument..."):
                try:
                    # Bildoptimierung (Wichtig für Fotos von Papier)
                    gray = ImageOps.grayscale(img)
                    enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                    # Texterkennung (Deutsch & Spanisch kombiniert)
                    extrakt = pytesseract.image_to_string(enhanced, lang='deu+spa')
                    st.session_state['text_inhalt'] = extrakt
                    st.success("Analyse abgeschlossen!")
                except Exception as e:
                    st.error(f"Fehler: Prüfe die 'packages.txt' in GitHub! ({e})")

    with col_rech:
        # Externer Recherche-Link (Dublettenprüfung)
        st.markdown(f"### [🔍 Dubletten-Check bei Google](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")

# 3. INTERAKTIVE FUNKTIONEN (Nur sichtbar nach Analyse)
if st.session_state['text_inhalt']:
    st.divider()
    
    tab1, tab2 = st.tabs(["💬 Chat & Fragen", "📍 Karte & Rohdaten"])
    
    with tab1:
        st.subheader("Fragen zum Objekt")
        frage = st.text_input("z.B. 'Wie groß ist das Grundstück?' oder 'Bohrbrunnen?'")
        
        if frage:
            f_low = frage.lower()
            t_low = st.session_state['text_inhalt'].lower()
            
            if f_low in t_low:
                st.success("Gefunden! Hier ist der relevante Ausschnitt:")
                pos = t_low.find(f_low)
                st.info(f"... {st.session_state['text_inhalt'][max(0, pos-60):pos+120]} ...")
            else:
                st.warning("Keine direkte Übereinstimmung im Scan gefunden.")

    with tab2:
        # Standard-Karte Málaga
        st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
        with st.expander("Vollständiges Scan-Protokoll"):
            st.code(st.session_state['text_inhalt'])
