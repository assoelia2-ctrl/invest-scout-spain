import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

st.set_page_config(page_title="Invest-Scout: Screenshot-Modus", layout="wide")

if 'text' not in st.session_state:
    st.session_state['text'] = ""

st.title("🛡️ Invest-Scout: Screenshot-Analyse")

# Stabiler Uploader für Screenshots
datei = st.file_uploader("Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="sc_v1")

if datei is not None:
    try:
        img = Image.open(datei)
        st.image(img, caption="Screenshot erkannt", use_container_width=True)
        
        if st.button("🚀 SCREENSHOT ANALYSIEREN"):
            # Kontrast für Screenshots optimieren
            proc = ImageOps.grayscale(img)
            proc = ImageEnhance.Contrast(proc).enhance(1.5)
            
            text = pytesseract.image_to_string(proc, lang='deu+spa')
            st.session_state['text'] = text
            st.success("Analyse erfolgreich!")
    except Exception as e:
        st.error(f"Fehler: {e}")

if st.session_state['text']:
    st.divider()
    st.write("### Gelesener Text:")
    st.info(st.session_state['text'])
    st.markdown(f"### [🔍 Dubletten-Recherche starten](https://www.google.com/search?q=Málaga+Immobilie+Check)")
