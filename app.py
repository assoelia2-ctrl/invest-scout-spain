import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract
import pandas as pd

st.set_page_config(page_title="Málaga Invest: Detail-Retter", layout="wide")

if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = ""

st.title("🛡️ Invest-Scout: Foto-Optimierung")

file = st.file_uploader("Bild hochladen (95KB+):", type=["jpg", "png", "jpeg"], key="fix_95kb")

if file:
    img = Image.open(file)
    st.image(img, caption="Originalbild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI schärft das Foto..."):
            try:
                # RETTUNG FÜR KLEINE DATEIEN:
                # 1. Bild künstlich vergrößern (Resampling), damit OCR mehr Pixel hat
                img = img.resize((img.width * 2, img.height * 2), resample=Image.LANCZOS)
                
                # 2. Graustufen & Schärfen
                proc = ImageOps.grayscale(img)
                proc = proc.filter(ImageFilter.SHARPEN)
                
                # 3. Kontrast extrem erhöhen (macht Pixel-Matsch zu klarem Schwarz/Weiß)
                proc = ImageEnhance.Contrast(proc).enhance(3.0)
                
                # Texterkennung
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['doc_text'] = text
                st.success("Analyse abgeschlossen!")
            except Exception as e:
                st.error(f"Fehler: {e}")

if st.session_state['doc_text']:
    st.divider()
    st.subheader("💬 Ergebnisse & Recherche")
    st.markdown("### [🔍 Dubletten-Check](https://www.google.com/search?q=Málaga+Immobilie+Invest)")
    
    with st.expander("Gelesener Text"):
        st.write(st.session_state['doc_text'])
