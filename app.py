import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import re

st.set_page_config(page_title="Málaga Invest Scout", layout="wide", page_icon="🏠")

if 'scan_data' not in st.session_state:
    st.session_state['scan_data'] = ""

st.title("🏠 Málaga Invest: Finaler Scout")

# Stabiler Uploader für Screenshots
uploaded_file = st.file_uploader("Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="final_v1")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Dokument geladen", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI extrahiert Daten..."):
            proc = ImageOps.grayscale(img)
            proc = ImageEnhance.Contrast(proc).enhance(1.8)
            text = pytesseract.image_to_string(proc, lang='deu+spa')
            st.session_state['scan_data'] = text

if st.session_state['scan_data']:
    raw_text = st.session_state['scan_data']
    st.divider()
    
    # Extraktion der Key-Facts
    found_afo = "✅" if "AFO" in raw_text.upper() else "⚠️"
    found_water = "💧" if any(x in raw_text.lower() for x in ["pozo", "agua", "brunnen"]) else "❓"
    found_m2 = re.findall(r'\d+[\d.,]*\s?m[2²]', raw_text)

    col1, col2, col3 = st.columns(3)
    col1.metric("Grundstück", found_m2[0] if found_m2 else "N/A")
    col2.metric("AFO Status", found_afo)
    col3.metric("Wasser", found_water)

    st.link_button("🔍 Dubletten-Check bei Google", f"https://www.google.com/search?q=Malaga+Immobilie+Check")
    with st.expander("Rohdaten anzeigen"):
        st.code(raw_text)
