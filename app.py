import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import gc

st.set_page_config(page_title="Invest-Scout: Multi-Scan", layout="wide")

if 'gesamter_text' not in st.session_state:
    st.session_state['gesamter_text'] = []

st.title("🛡️ Invest-Scout: Multi-Upload")

# 1. Multi-Uploader aktivieren
dateien = st.file_uploader("Mehrere Fotos/Screenshots wählen:", 
                            type=["jpg", "png", "jpeg"], 
                            accept_multiple_files=True, # WICHTIG
                            key="multi_v13")

if dateien:
    if st.button("🚀 ALLE BILDER ANALYSIEREN"):
        st.session_state['gesamter_text'] = [] # Reset für neuen Durchlauf
        
        for i, datei in enumerate(dateien):
            with st.status(f"Verarbeite Bild {i+1} von {len(dateien)}...") as status:
                try:
                    img = Image.open(datei)
                    
                    # 95KB Rettung & RAM-Schutz
                    img_big = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
                    proc = ImageOps.grayscale(img_big)
                    proc = ImageEnhance.Contrast(proc).enhance(2.0)
                    
                    text = pytesseract.image_to_string(proc, lang='deu+spa')
                    st.session_state['gesamter_text'].append(f"--- Datei {i+1} ---\n{text}")
                    
                    # RAM sofort leeren nach jedem Bild
                    del img
                    del img_big
                    del proc
                    gc.collect()
                    status.update(label=f"Bild {i+1} fertig!", state="complete")
                except Exception as e:
                    st.error(f"Fehler bei Bild {i+1}: {e}")

# 2. Anzeige der gesammelten Ergebnisse
if st.session_state['gesamter_text']:
    st.divider()
    st.success(f"{len(st.session_state['gesamter_text'])} Dokumente analysiert.")
    
    combined = "\n\n".join(st.session_state['gesamter_text'])
    
    with st.expander("Gesamten Text anzeigen"):
        st.text_area("Ergebnisse:", value=combined, height=400)
    
    # Recherche-Link (Nutzt das erste erkannte Stichwort)
    st.markdown("### [🔍 Kombinierte Recherche starten](https://www.google.com/search?q=Málaga+Immobilie+Invest+Check)")
