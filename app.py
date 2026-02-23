import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# 1. Seite stabilisieren
st.set_page_config(page_title="Invest-Scout Fix", layout="wide")

# Speicher für den Text sicherstellen
if 'mein_text' not in st.session_state:
    st.session_state['mein_text'] = ""

st.title("🛡️ Invest-Scout: Foto- & Screenshot-Modus")

# 2. Der Uploader (mit Sicherheits-Abfrage gegen NameError)
# Wir nutzen einen neuen Key, um alte Fehler zu löschen
up_file = st.file_uploader("Bild oder Foto auswählen:", type=["jpg", "png", "jpeg"], key="safe_v5")

if up_file is not None:
    # Das Bild laden
    img = Image.open(up_file)
    st.image(img, caption="Datei erfolgreich erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI liest Dokument..."):
            try:
                # RETTUNG FÜR FOTOS: Wir vergrößern das Bild für die KI
                # Das hilft besonders bei 95 KB Fotos
                w, h = img.size
                img_big = img.resize((w*2, h*2), Image.Resampling.LANCZOS)
                
                # Vorverarbeitung (Graustufen & Kontrast)
                proc = ImageOps.grayscale(img_big)
                proc = ImageEnhance.Contrast(proc).enhance(2.0)
                
                # OCR (Texterkennung)
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['mein_text'] = text
                st.success("Erfolg! Daten ausgelesen.")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 3. Anzeige (Nur wenn Text da ist)
if st.session_state['mein_text']:
    st.divider()
    st.subheader("💬 Ergebnisse")
    
    # Recherche-Link
    st.markdown("### [🔍 Dubletten im Internet prüfen](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")
    
    with st.expander("Gelesenen Text anzeigen"):
        st.write(st.session_state['mein_text'])
