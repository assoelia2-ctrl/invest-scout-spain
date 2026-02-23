import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Andalusia Real Estate Scout", layout="wide")

def main():
    st.title("☀️ Andalusien Investment-Analysator")
    st.subheader("Regionaler Report-Generator")
    
    st.info("Benennungsschema: PROVINZ_STADT_PREIS_FLAECHE (z.B. Malaga_Estepona_400000_100)")
    
    Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg'])

    if Dateien:
        # Daten vorverarbeiten und nach Provinzen gruppieren
        daten_pool = {}
        for d in Dateien:
            try:
                parts = d.name.split('.')[0].split('_')
                provinz = parts[0].capitalize()
                stadt = parts[1].replace('-', ' ')
                preis = float(parts[2])
                flaeche = float(parts[3])
                
                if provinz not in daten_pool:
                    daten_pool[provinz] = []
                
                daten_pool[provinz].append({
                    "stadt": stadt,
                    "preis": preis,
                    "flaeche": flaeche,
                    "qm_preis": preis / flaeche,
                    "file": d
                })
            except:
                st.warning(f"Datei ignoriert (falsches Schema): {d.name}")

        if daten_pool and st.button("Andalusien-Report generieren"):
            pdf = FPDF()
            
            # --- TITELSEITE ---
            pdf.add_page()
            pdf.set_font("Arial", 'B', 24)
            pdf.ln(60)
            pdf.cell(0, 20, "Investment-Analyse Andalusien", ln=1, align='C')
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, f"Zusammenfassung von {len(Dateien)} Objekten", ln=1, align='C')

            # --- REGIONALE ÜBERSICHTEN ---
            for provinz, objekte in sorted(daten_pool.items()):
                pdf.add_page()
                pdf.set_font("Arial", 'B', 18)
                pdf.cell(0, 15, f"Provinz: {provinz}", ln=1)
                
                # Tabellen-Header
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(50, 10, "Stadt", 1)
                pdf.cell(40, 10, "Preis", 1)
                pdf.cell(40, 10, "m2", 1)
                pdf.cell(40, 10, "Euro/m2", 1, ln=1)
                
                pdf.set_font("Arial", size=10)
                prov_gesamt = 0
                
                for obj in objekte:
                    pdf.cell(50, 10, obj['stadt'], 1)
                    pdf.cell(40, 10, f"{obj['preis']:,.0f} €", 1)
                    pdf.cell(40, 10, f"{obj['flaeche']} m2", 1)
                    pdf.cell(40, 10, f"{obj['qm_preis']:,.2f} €", 1, ln=1)
                    prov_gesamt += obj['preis']
                
                pdf.ln(5)
                avg_qm = sum(o['qm_preis'] for o in objekte) / len(objekte)
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, f"Ø Quadratmeterpreis in {provinz}: {avg_qm:,.2f} €/m2", ln=1)

                # --- BILDER DER PROVINZ ---
                for obj in objekte:
                    temp_name = f"temp_{obj['file'].name}"
                    with open(temp_name, "wb") as f:
                        f.write(obj['file'].getbuffer())
                    
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(0, 10, f"{provinz}: {obj['stadt']} - {obj['preis']:,.0f} €", ln=1, align='C')
                    pdf.image(temp_name, x=10, y=25, w=190)
                    os.remove(temp_name)
            
            pdf.output("Andalusien_Investment_Report.pdf")
            st.success("Andalusien-Report fertig erstellt!")
            
            with open("Andalusien_Investment_Report.pdf", "rb") as f:
                st.download_button("📩 Gesamten Report herunterladen", f, "Andalusien_Investment_Report.pdf")

if __name__ == "__main__":
    main()
