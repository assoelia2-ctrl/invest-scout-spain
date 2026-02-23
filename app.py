import streamlit as st
from fpdf import FPDF
import os

# App-Konfiguration
st.set_page_config(page_title="Andalusien Invest Pro", layout="wide")

def main():
    st.title("☀️ Andalusien Real Estate Scout")
    st.subheader("Analyse-Tool für Investment-Objekte")

    # 1. Datei-Upload
    st.info("Lade hier deine Screenshots hoch (z.B. aus Idealista oder Fotocasa).")
    Dateien = st.file_uploader("Screenshots auswählen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    objekt_liste = []

    if Dateien:
        st.write(f"---")
        st.subheader("📋 Daten-Check & Finanz-Eingabe")
        st.write("Bitte ergänze die Daten für die Kalkulation:")
        
        # Formular für jedes Bild
        for i, d in enumerate(Dateien):
            # Vorbefüllung versuchen, falls Dateiname Schema hat: Provinz_Stadt_Preis_m2
            parts = d.name.split('.')[0].split('_')
            v_prov = parts[0].capitalize() if len(parts) > 0 else "Malaga"
            v_stadt = parts[1].replace('-', ' ') if len(parts) > 1 else "Unbekannt"
            v_preis = float(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0.0
            v_flaeche = float(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0.0

            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                prov = st.selectbox(f"Provinz ({i})", 
                                    ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], 
                                    index=["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"].index(v_prov) if v_prov in ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"] else 6,
                                    key=f"prov_{i}")
            with col2:
                stadt = st.text_input(f"Stadt/Lage ({i})", v_stadt, key=f"stadt_{i}")
            with col3:
                preis = st.number_input(f"Kaufpreis € ({i})", value=v_preis, step=5000.0, key=f"preis_{i}")
            with col4:
                flaeche = st.number_input(f"Fläche m² ({i})", value=v_flaeche, step=1.0, key=f"m2_{i}")
            
            objekt_liste.append({
                "prov": prov, 
                "stadt": stadt, 
                "preis": preis, 
                "flaeche": flaeche, 
                "file": d
            })
            st.divider()

        # 2. PDF-Generierung
        if st.button("🚀 Gesamten Andalusien-Report erstellen"):
            if not objekt_liste:
                st.error("Keine Daten vorhanden.")
                return

            with st.spinner("Kalkuliere Steuern und erstelle PDF..."):
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)

                # Gruppieren nach Provinzen für die Kapitelstruktur
                provinzen_im_set = sorted(list(set([o["prov"] for o in objekt_liste])))
                
                # TITELSEITE
                pdf.add_page()
                pdf.set_font("Arial", 'B', 25)
                pdf.ln(80)
                pdf.cell(0, 20, "INVESTMENT-ANALYSE", ln=1, align='C')
                pdf.set_font("Arial", '', 18)
                pdf.cell(0, 15, "Immobilienmarkt Andalusien", ln=1, align='C')
                pdf.set_font("Arial", 'I', 12)
                pdf.cell(0, 10, "Erstellt mit der Scout-App", ln=1, align='C')

                for p in provinzen_im_set:
                    # KAPITEL-SEITE PRO PROVINZ
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 20)
                    pdf.cell(0, 20, f"Provinz: {p}", ln=1)
                    pdf.ln(5)
                    
                    prov_objekte = [o for o in objekt_liste if o["prov"] == p]
                    
                    for obj in prov_objekte:
                        # FINANZ-KALKULATION
                        kaufpreis = obj["preis"]
                        itp_steuer = kaufpreis * 0.07  # 7% ITP in Andalusien
                        nebenkosten = kaufpreis * 0.015 # Notar/Register ca. 1.5%
                        total_investment = kaufpreis + itp_steuer + nebenkosten
                        qm_preis = kaufpreis / obj["flaeche"] if obj["flaeche"] > 0 else 0

                        # Detail-Block im PDF
                        pdf.set_font("Arial", 'B', 14)
                        pdf.set_fill_color(240, 240, 240)
                        pdf.cell(0, 12, f"Objekt: {obj['stadt']}", ln=1, fill=True)
                        
                        pdf.set_font("Arial", '', 11)
                        pdf.cell(95, 8, f"Kaufpreis: {kaufpreis:,.2f} EUR", 0)
                        pdf.cell(95, 8, f"Flaeche: {obj['flaeche']} m2", ln=1)
                        
                        pdf.cell(95, 8, f"Steuern (7% ITP): {itp_steuer:,.2f} EUR", 0)
                        pdf.cell(95, 8, f"Preis/m2: {qm_preis:,.2f} EUR/m2", ln=1)
                        
                        pdf.cell(95, 8, f"Notar/Register (ca.): {nebenkosten:,.2f} EUR", 0)
                        pdf.set_font("Arial", 'B', 11)
                        pdf.cell(95, 8, f"GESAMT-KAPITAL: {total_investment:,.2f} EUR", ln=1)
                        pdf.ln(5)

                        # Bild einfügen
                        t_name = f"temp_{obj['file'].name}"
                        with open(t_name, "wb") as f:
                            f.write(obj["file"].getbuffer())
                        
                        # Bild auf der gleichen oder nächsten Seite (skaliert)
                        pdf.image(t_name, x=10, y=pdf.get_y(), w=180)
                        pdf.ln(130) # Platz für das Bild lassen
                        
                        os.remove(t_name)
                        
                        # Falls das Bild zu nah am Ende ist, neue Seite
                        if pdf.get_y() > 200:
                            pdf.add_page()

                # Speichern und Download
                report_name = "Andalusien_Investment_Report.pdf"
                pdf.output(report_name)
                
                st.success("✅ Report erfolgreich generiert!")
                with open(report_name, "rb") as f:
                    st.download_button("📩 PDF-Dossier herunterladen", f, file_name=report_name)

if __name__ == "__main__":
    main()
