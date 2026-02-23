import streamlit as st
import requests
import base64
from PIL import Image
import io
from fpdf import FPDF

st.set_page_config(page_title="Málaga Invest: UNSTOPPABLE", layout="wide")

# API Key abrufen
api_key = st.secrets.get("GEMINI_API_KEY")

def analyze_images_direct(images, prompt):
    # Wir erzwingen hier die stabile v1 Schnittstelle manuell!
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    parts = [{"text": prompt}]
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(buf.getvalue()).decode("utf-8")
            }
        })
    
    payload = {"contents": [{"parts": parts}]}
    response = requests.post(url, json=payload)
    return response.json()

st.title("🛡️ Invest-Scout: Direkt-Anbindung")

files = st.file_uploader("Screenshots:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if files and st.button("🚀 ANALYSE ERZWINGEN"):
    with st.spinner("Breche Blockade auf..."):
        try:
            imgs = [Image.open(f) for f in files]
            prompt = "Expertencheck Málaga: AFO-Status, Rústico/Urbano, Preis-Check m2 und klares Risiko-Fazit."
            
            result = analyze_images_direct(imgs, prompt)
            
            # Ergebnis extrahieren
            if "candidates" in result:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                st.session_state["final_res"] = text
                st.markdown(text)
            else:
                st.error(f"Google verweigert Zugriff: {result}")
        except Exception as e:
            st.error(f"Fehler: {e}")

if "final_res" in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=st.session_state["final_res"].encode('latin-1', 'replace').decode('latin-1'))
    st.download_button("📄 PDF Speichern", data=bytes(pdf.output()), file_name="Analyse.pdf")
