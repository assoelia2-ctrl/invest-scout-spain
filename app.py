import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# 1. Radikale Absicherung des Speichers
st.set_page_config(page_title="Invest-Scout Fix", layout="wide")

# Wir legen leere Variablen fest, damit es keinen 'NameError' geben kann
if 'ocr_text' not in st.session_state:
    st.session_state['ocr_text'] = ""

st.title("🛡️ Invest-Scout: Finaler Fix")

# 2. Der Uploader (mit einem neuen, frischen Key)
# Wir nennen die Variable jetzt 'up_file', um alte Konflikte zu lösen
up_file = st.file_uploader("Bild hier hochladen:", type=["jpg", "png", "jpeg"], key="stable_v4")

if up_file is not None:
    # Bild laden
    img = Image.open(up_file)
    st.image(img, caption="Datei geladen", use_container_width=True)
    
    # Der Analyse-Knopf
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI arbeitet..."):
            try:
                # RETTUNG FÜR KLEINE FOTOS: 
                # Wir skalieren das Bild massiv hoch, damit die KI Pixel erkennt
                new_size = (img.width * 3, img.height * 3)
                img_big = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Vorverarbeitung
                gray = ImageOps.grayscale(img_big)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.5)
                
                # Texterkennung
                result = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['ocr_text'] = result
                st.success("Erfolg!")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 3. Chat & Recherche (nur wenn Text da ist)
if st.session_state['ocr_text']:
    st.divider()
    
    # Recherche-Link (Extern, damit die App nicht abstürzt)
    st.markdown("### [🔍 Dubletten im Internet suchen](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    # Einfaches Chat-Feld
    frage = st.text_input("Frag nach Details (z.B. Bohrbrunnen):", key="chat_input")
    if frage:
        if frage.lower() in st.session_state['ocr_text'].lower():
            st.success("✅ Gefunden!")
            st.write(st.session_state['ocr_text'])
        else:
            st.warning("Kein Treffer im Text.")
