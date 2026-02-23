import streamlit as st
import requests
import base64
from PIL import Image
import io
from fpdf import FPDF

# --- SETUP ---
st.set_page_config(page_title="Málaga Invest: FORCE", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY")

def analyze_direct(image_files, prompt_text):
    # WIR ERZWINGEN HIER DIE STABILE V1 VERSION MANUELL
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    parts = [{"text": prompt_text}]
    for f in image_files:
        img_data = base64.b64encode(f.getvalue()).decode("utf-8")
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": img_data
            }
        })
    
    payload = {"contents": [{"parts": parts}]}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# --- UI ---
st.title("🛡️ Invest-Scout: Erzwinge Verbindung")
st.write("Diese Version umgeht alle fehlerhaften Bibliotheken.")

files = st.file_uploader("Screenshots:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if files and st.button("🚀 ANALYSE JETZT ERZWINGEN"):
    with st.spinner("Direktverbindung zu Google wird aufgebaut..."):
        prompt = "Analysiere als Malaga-Experte: AFO-Status, Rústico/Urbano, Preis m2 und Risiko-Fazit."
        result = analyze_direct(files, prompt)
        
        if "candidates" in result:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            st.session_state["final_text"] = answer
            st.markdown(answer)
        else:
            st.error(f"Google meldet Fehler: {result}")
            st.info("Überprüfe, ob der API-Key in den Secrets korrekt gespeichert ist.")

if "final_text" in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean = st.session_state["final_text"].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean)
    st.download_button("📄 Bericht speichern", data=bytes(pdf.output()), file_name="Analyse.pdf")
