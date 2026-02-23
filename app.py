import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Andalusia Invest", layout="wide")

def main():
    st.title("☀️ Andalusien Investment-Scount")
    
    # 1. Upload
    Dateien = st.file_uploader("Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg'])
    
    objekt_liste = []

    if Dateien:
        st.subheader("Daten-Check & Ergänzung")
        st.write("Bitte kurz prüfen oder ergänzen, damit die Analyse stimmt:")
        
        for i, d in enumerate(Dateien):
            # Versuche Daten aus Name zu lesen
            parts = d.name.split('.')[0].split('_')
            v_prov = parts[0] if len(parts) > 0 else "Unbekannt"
            v_stadt = parts[1] if len(parts) > 1 else "Stadt"
            v_preis = float(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0.0
            v_flaeche = float(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0.0

            # UI für Korrekturen
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                prov = st.selectbox(f"Provinz ({i})", ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], 
                                    index=["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"].index(v_prov) if v_prov in ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"] else 6)
            with col2:
                stadt = st.text_input(f"Stadt ({i})", v_stadt)
            with col3:
                preis = st.number_input(f"Preis € ({i})", value=v_preis, step=1000.0)
            with col4:
                flaeche = st.number_input(f"m2 ({i})", value=v_flaeche, step=1.0)
            
            objekt_liste.append({"prov": prov, "stadt": stadt, "preis": preis, "flaeche": flaeche, "file": d})
            st.divider()

        # 2. PDF Generierung
        if st.button("Andalusien-Report mit korrigierten Daten erstellen"):
            pdf = FPDF()
            # Gruppieren nach Provinz
            provinzen = sorted(list(set([o["prov"] for o in objekt_liste])))
            
            for p in provinzen:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, "Region: " + p, ln=1)
                
                prov_objekte = [o for o in objekt_liste if o["prov"] == p]
                for obj in prov_objekte:
                    # Bild kurz speichern
                    t_name = "temp_" + obj["file"].name
                    with open(t_name, "wb") as f:
                        f.write(obj["file"].getbuffer())
                    
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, obj["stadt"] + " - " + str(obj["preis"]) + " Euro", ln=1)
                    pdf.image(t_name, x=10, y=25, w=190)
                    os.remove(t_name)

            pdf.output("Andalusien_Report.pdf")
            st.success("Report fertig!")
            with open("Andalusien_Report.pdf", "rb") as f:
                st.download_button("Download Report", f, "Andalusien_Report.pdf")

if __name__ == "__main__":
    main()
