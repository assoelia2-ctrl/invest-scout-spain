import streamlit as st
from fpdf import FPDF
import os

# Einfache Konfiguration
st.set_page_config(page_title="Malaga App")

def main():
    st.title("🌴 Malaga Dossier")
    
    # Bilder direkt hochladen - löst das Ordner-Problem
    st.info("Bilder hier auswählen:")
    Dateien = st.file_uploader("Screenshots laden", accept_multiple_files=True, type=['png', 'jpg'])

    if Dateien:
        st.write("Anzahl Bilder:", len(Dateien))
        
        if st.button("PDF Erstellen"):
            pdf = FPDF()
            
            for d in Dateien:
                # Bild kurz zwischenspeichern
                name = "temp_" + d.name
                with open(name, "wb") as f:
                    f.write(d.getbuffer())
                
                pdf.add_page()
                # Titel ohne komplizierte f-strings
                titel = d.name.split('.')[0]
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, txt=titel, ln=1, align='C')
                
                # Bild einfügen
                pdf.image(name, x=10, y=25, w=190)
                os.remove(name)
            
            pdf.output("Bericht.pdf")
            st.success("PDF fertig!")
            
            with open("Bericht.pdf", "rb") as f:
                st.download_button("Datei Herunterladen", f, "Bericht.pdf")

if __name__ == "__main__":
    main()
