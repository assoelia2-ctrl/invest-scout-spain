import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# 1. SYSTEM-CHECK & SPEICHER
st.set_page_config(page_title="Invest-Scout: Final Fix", layout="wide")

# Wir erzwingen, dass diese Variablen ab Sekunde 1 existieren
if 'ocr_inhalt' not in st.session_state:
    st.session_state['ocr_inhalt'] = ""

st.title("🛡️ Invest-Scout: Foto-Garantie")

# 2. STABILER UPLOADER
# Wir weisen das Ergebnis direkt einer Session-Variable zu
up_file = st.file_uploader("Bild oder Foto hier rein:", type=["jpg", "png", "jpeg"], key="ultra_stable_v11")

# 3. VERARBEITUNG
if up_file:
    # Das Bild wird sofort geladen
    img = Image.open(up_file)
    st.image(img, caption="Datei erfolgreich geladen", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI liest Dokument..."):
            try:
                # 95KB RETTUNG: Wir vergrößern das Bild massiv
                # Das macht Pixel-Matsch für die KI wieder lesbar
                w, h = img.size
                img_big = img.resize((w*3, h*3), Image.Resampling.LANCZOS)
                
                # Kontrast-Kurve für Fotos
                proc = ImageOps.grayscale(img_big)
                proc = ImageEnhance.Contrast(proc).enhance(2.5)
                
                # Texterkennung
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['ocr_inhalt'] = text
                st.success("Analyse fertig!")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 4. RECHERCHE (Immer sichtbar, sobald Text existiert)
if st.session_state['ocr_inhalt']:
    st.divider()
    st.subheader("🔍 Recherche-Ergebnisse")
    
    # Sicherer Recherche-Link
    st.markdown("### [👉 Dubletten im Internet prüfen](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    with st.expander("Gelesene Daten (Rohtext)"):
        st.write(st.session_state['ocr_inhalt'])
