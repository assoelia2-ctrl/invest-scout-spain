import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# 1. Speicher felsenfest vordefinieren
st.set_page_config(page_title="Invest-Scout: Profi-Fix", layout="wide")

if 'text_daten' not in st.session_state:
    st.session_state['text_daten'] = ""

st.title("🛡️ Invest-Scout: Foto-Garantie")

# 2. Uploader OHNE Zwischenvariable (verhindert den NameError)
st.file_uploader("Bild oder Foto hier rein:", type=["jpg", "png", "jpeg"], key="dateiupload")

# 3. Direkter Zugriff auf den Speicherplatz des Uploaders
if st.session_state.dateiupload is not None:
    # Bild laden
    img = Image.open(st.session_state.dateiupload)
    st.image(img, caption="Datei erfolgreich geladen", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI liest Dokument..."):
            try:
                # 95KB RETTUNG: Bild vergrößern für bessere Lesbarkeit
                img_big = img.resize((img.width * 3, img.height * 3), Image.Resampling.LANCZOS)
                
                # Kontrast optimieren
                proc = ImageOps.grayscale(img_big)
                proc = ImageEnhance.Contrast(proc).enhance(2.5)
                
                # Texterkennung
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['text_daten'] = text
                st.success("Analyse fertig!")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 4. RECHERCHE-LINK
if st.session_state['text_daten']:
    st.divider()
    st.markdown("### [👉 Dubletten im Internet prüfen](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    with st.expander("Gelesene Daten"):
        st.write(st.session_state['text_daten'])
