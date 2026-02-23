import streamlit as st
from gradio_client import Client
from PIL import Image
import io
from fpdf import FPDF

st.set_page_config(page_title="Málaga Invest: Independent")

st.title("🛡️ Invest-Scout (Google-Frei)")
st.info("Wir nutzen jetzt ein Open-Source Modell, um die Google-Blockade zu umgehen.")

uploaded_file = st.file_uploader("Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Bereit zur Analyse", width=300)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Open-Source KI analysiert das Bild..."):
            try:
                # Wir nutzen den Gradio Client, um das Modell 'Llava' anzusprechen
                client = Client("xtuner/llava-llama-3-8b")
                
                # Bild temporär speichern für den Upload
                img_path = "temp_img.jpg"
                img.save(img_path)
                
                result = client.predict(
                    image=img_path,
                    text="Analysiere diese Immobilie: Preis, m2, Zustand und AFO-Risiko.",
                    api_name="/predict"
                )
                
                st.session_state['res'] = result
                st.markdown("### 📋 Ergebnis")
                st.write(result)
            except Exception as e:
                st.error(f"Fehler bei der Open-Source KI: {e}")

# PDF Download bleibt gleich
if 'res' in st.session_state:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = st.session_state['res'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    st.download_button("📄 PDF Speichern", data=bytes(pdf.output()), file_name="Analyse.pdf")
