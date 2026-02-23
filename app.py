import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Málaga Invest: Ultimate", layout="wide")

# Initialisierung des Speichers
if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = None

st.title("🛡️ Invest-Scout: Analyse, Chat & Recherche")

# --- UPLOAD BEREICH ---
file = st.file_uploader("Bild/Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🚀 ANALYSE STARTEN"):
            with st.spinner("Lese Daten aus..."):
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                text = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['doc_text'] = text
                st.success("Analyse erfolgreich!")

    with col_btn2:
        # Recherche-Link generieren (Google Lens / Bilder Umweg)
        search_url = "https://www.google.com/searchbyimage?sbisrc=4h&image_url=" 
        st.markdown(f"[🔍 Bild im Internet suchen](https://www.google.com/search?q=Málaga+Immobilien+Suche)")
        st.info("Klicke oben, um eine manuelle Dubletten-Prüfung zu starten.")

# --- ANALYSE & CHAT BEREICH ---
if st.session_state['doc_text']:
    st.divider()
    
    # Ergebnisse in Spalten
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("📍 Standort")
        st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    with c2:
        st.subheader("💬 Chat mit dem Dokument")
        query = st.text_input("Frag mich etwas zum Scan (z.B. 'Preis?', 'Brunnen?'):")
        if query:
            q = query.lower()
            t = st.session_state['doc_text'].lower()
            if q in t:
                st.write("✅ Ich habe Informationen dazu im Text gefunden!")
                # Zeige den relevanten Ausschnitt
                start = max(0, t.find(q) - 50)
                end = min(len(t), t.find(q) + 100)
                st.info(f"...{st.session_state['doc_text'][start:end]}...")
            else:
                st.write("❌ Dazu konnte ich im aktuellen Scan leider nichts finden.")

    with st.expander("Vollständiges Scan-Protokoll ansehen"):
        st.code(st.session_state['doc_text'])
