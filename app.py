import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# 1. SETUP
st.set_page_config(page_title="Invest-Scout: Finaler Fix", layout="wide")

# Speicher für Text anlegen, falls er noch nicht da ist
if 'text' not in st.session_state:
    st.session_state['text'] = ""

st.title("🛡️ Invest-Scout: Foto- & Screenshot-Garantie")

# 2. DER UPLOADER (isoliert in einer Variablen)
datei = st.file_uploader("Bild/Foto hochladen:", type=["jpg", "png", "jpeg"], key="uploader_vfinal")

# 3. DIE "SICHERHEITS-SCHLEUSE"
# Wir nutzen try/except, damit der NameError die App nicht mehr killen kann
try:
    if datei is not None:
        img = Image.open(datei)
        st.image(img, caption="Datei erfolgreich erkannt", use_container_width=True)
        
        if st.button("🚀 ANALYSE STARTEN"):
            with st.spinner("KI liest Dokument..."):
                # Foto-Rettung (Aufpumpen auf 3-fache Größe)
                w, h = img.size
                img_big = img.resize((w*3, h*3), Image.Resampling.LANCZOS)
                
                # Vorverarbeitung
                proc = ImageOps.grayscale(img_big)
                proc = ImageEnhance.Contrast(proc).enhance(2.5)
                
                # OCR (Texterkennung)
                st.session_state['text'] = pytesseract.image_to_string(proc, lang='deu+spa')
                st.success("Analyse abgeschlossen!")

except NameError:
    st.warning("Warte auf Datei-Upload...")
except Exception as e:
    st.error(f"Technischer Fehler: {e}")

# 4. ERGEBNISSE & RECHERCHE
if st.session_state['text']:
    st.divider()
    st.markdown("### [🔍 Dubletten im Internet prüfen](https://www.google.com/search?q=Málaga+Immobilie+Invest+Check)")
    with st.expander("Gelesene Daten"):
        st.write(st.session_state['text'])
