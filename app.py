import os
import streamlit as st
from fpdf import FPDF

# 1. App-Konfiguration (Leichtgewicht-Modus)
st.set_page_config(page_title="Málaga Immobilien-Dossier", layout="wide")

def main():
    st.title("🌴 Málaga Projekt: Dossier-Generator")
    st.write("Status: App bereit. Warte auf Eingabe...")

    # Pfad zu deinen Screenshots (Pydroid Standard-Pfad oder relativ)
    # Nutze '.' für den aktuellen Ordner, in dem das Skript liegt
    img_dir = "./screenshots" 

    # 2. Sicherheitscheck: Existiert der Ordner?
    if not os.path.exists(img_dir):
        st.error(f"Ordner '{img_dir}' nicht gefunden. Bitte erstelle ihn!")
        return

    # 3. UI-Elemente
    if st.button("🔍 Screenshots scannen & PDF erstellen"):
        with st.spinner("Verarbeite Bilder... bitte warten."):
            try:
                # Bilder suchen
                images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg'))]
                
                if not images:
                    st.warning("Keine Bilder im Ordner gefunden.")
                else:
                    # PDF Logik (Minimalistisch)
                    pdf = FPDF()
                    for img in images:
                        pdf.add_page()
                        clean_name = img.replace('_', ' ').split('.')[0]
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt=clean_name, ln=1, align='C')
                        pdf.image(os.path.join(img_dir, img), x=10, y=25, w=190)
                    
                    output_file = "Malaga_Analyse.pdf"
                    pdf.output(output_name := output_file)
                    st.success(f"✅ Fertig! Datei gespeichert als: {output_name}")
                    
            except Exception as e:
                st.error(f"Fehler aufgetreten: {str(e)}")

if __name__ == "__main__":
    main()
