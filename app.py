import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Malaga Pro")

def main():
    st.title("🌴 Málaga Investment-Analysator")
    
    Dateien = st.file_uploader("Screenshots hochladen (Schema: Stadtteil_Preis_Flaeche)", 
                               accept_multiple_files=True, type=['png', 'jpg'])

    if Dateien:
        if st.button("Analyse & PDF erstellen"):
            pdf = FPDF()
            pdf.add_page()
            
            # --- TABELLE & STATISTIK ---
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Marktanalyse Zusammenfassung", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(60, 10, "Lage", 1)
            pdf.cell(40, 10, "Preis", 1)
            pdf.cell(40, 10, "Flaeche", 1)
            pdf.cell(40, 10, "Euro/m2", 1, ln=1)
            
            pdf.set_font("Arial", size=11)
            
            gesamt_preis = 0
            anzahl = 0

            # Erster Durchlauf für die Tabelle
            for d in Dateien:
                try:
                    # Zerlegen des Namens: Stadtteil_Preis_Flaeche.png
                    parts = d.name.split('.')[0].split('_')
                    lage = parts[0]
                    preis = float(parts[1])
                    flaeche = float(parts[2])
                    qm_preis = preis / flaeche
                    
                    pdf.cell(60, 10, lage, 1)
                    pdf.cell(40, 10, str(preis) + " €", 1)
                    pdf.cell(40, 10, str(flaeche) + " m2", 1)
                    pdf.cell(40, 10, str(round(qm_preis, 2)) + " €", 1, ln=1)
                    
                    gesamt_preis += preis
                    anzahl += 1
                except:
                    continue # Falls Name nicht passt, Zeile überspringen

            if anzahl > 0:
                pdf.ln(5)
                pdf.set_font("Arial", 'I', 11)
                pdf.cell(0, 10, "Durchschnittlicher Preis: " + str(round(gesamt_preis/anzahl, 2)) + " €", ln=1)

            # --- BILDER-SEITEN ---
            for d in Dateien:
                name = "temp_" + d.name
                with open(name, "wb") as f:
                    f.write(d.getbuffer())
                
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, d.name.split('.')[0].replace('_', ' '), ln=1, align='C')
                pdf.image(name, x=10, y=25, w=190)
                os.remove(name)
            
            pdf.output("Malaga_Analyse.pdf")
            st.success("Analyse abgeschlossen!")
            
            with open("Malaga_Analyse.pdf", "rb") as f:
                st.download_button("Analyse-Report herunterladen", f, "Malaga_Analyse.pdf")

if __name__ == "__main__":
    main()
