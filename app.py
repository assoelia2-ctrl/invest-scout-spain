import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# ... dein bisheriger Code ...

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # NEU: FOTO-OPTIMIERUNG (Verhindert Abstürze bei großen Dateien)
    # Wenn das Bild sehr groß ist, skalieren wir es runter
    if img.width > 2000 or img.height > 2000:
        img.thumbnail((1500, 1500))
    
    st.image(img, caption="Bild für Analyse bereit", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI verarbeitet Foto..."):
            try:
                # Vorverarbeitung für Fotos (Kontrast erhöhen, Graustufen)
                img_proc = ImageOps.grayscale(img)
                img_proc = ImageEnhance.Contrast(img_proc).enhance(2.0)
                
                # Texterkennung mit Fehlerpuffer
                text = pytesseract.image_to_string(img_proc, lang='deu+spa')
                st.session_state['ergebnis_text'] = text
                st.success("Foto erfolgreich ausgelesen!")
            except Exception as e:
                st.error(f"Fehler bei Foto-Verarbeitung: {e}")
                st.info("Tipp: Versuche, das Foto mit weniger Auflösung zu machen.")
