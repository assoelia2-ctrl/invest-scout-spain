import streamlit as st
from fpdf import FPDF
import os

# App-Konfiguration für mobile Endgeräte
st.set_page_config(page_title="Málaga Dossier Generator", layout="centered")

def main():
    st.title("🌴 Málaga Immobilien-Projekt")
    st.subheader("Dossier-Generator (Direkt-Upload)")
    
    st.info("Nutze diese Version, um Bilder direkt vom Handy auszuwählen. Du musst keine Ordner mehr manuell erstellen.")

    # 1. Datei-Uploader (Mehrere Bilder gleichzeitig möglich)
    uploaded_files = st.file_uploader(
        "Wähle deine Screenshots aus", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg']
    )

    if uploaded_files:
        st.write(f"✅ {len(uploaded_files)} Bilder ausgewählt.")
        
        # Name für das fertige PDF
        pdf_filename = st.text_input("Dateiname für das PDF:", "Malaga_Investment_Report.pdf")

        if st.button("🚀 PDF jetzt generieren"):
            with st.spinner("Erstelle Dossier..."):
                try:
                    pdf = FPDF()
                    
                    for uploaded_file in uploaded_files:
                        # Temporäres Speichern des Bildes für FPDF
                        temp_name = f"temp_{uploaded_file.name}"
                        with open(temp_name, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Neue Seite im PDF
                        pdf.add_page()
                        
                        # Titel aus dem Dateinamen (schön formatiert)
                        title = uploaded_file.name.replace('_', ' ').split('.')[0]
                        pdf.set_font("Arial", 'B', size=14)
                        pdf.cell(0, 10, txt=title, ln=1, align='C')
                        
                        # Bild einfügen (skaliert auf A4 Breite)
                        pdf.image(temp_name, x=10, y=25, w=190)
                        
                        # Temporäre Datei löschen (Speicher sparen)
                        os.remove(temp_name)
                    
                    # PDF erstellen
                    pdf.output(pdf_filename)
                    
                    st.success(f"Dossier '{pdf_filename}' erfolgreich erstellt!")
                    
                    # Download-Button anzeigen
                    with open(pdf_filename, "rb") as file:
                        st.download_button(
                            label="⬇️ PDF herunterladen",
                            data=file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
                        
                except Exception as e:
                    st.error(f"Fe
