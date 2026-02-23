import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
import os
from PIL import Image

# --- KONFIGURATION ---
st.set_page_config(page_title="Andalusien AI Expert", layout="wide")

# Hier deinen Key eingeben oder über Sidebar steuern
api_key = st.sidebar.text_input("Gemini API Key eingeben", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Schnelles Vision-Modell

def analyze_image(img):
    """Sendet das Bild an die KI zur Investment-Analyse"""
    prompt = """
    Du bist ein erfahrener Immobilien-Gutachter in Andalusien. 
    Analysiere diesen Screenshot einer Immobilie/eines Grundstücks:
    1. Zustand von Dach und Fassade (Renovierungsstau?).
    2. Beurteilung der Zufahrt und des Geländes (Schatten, Boden).
    3. Solar-Potential (Dachausrichtung/Hindernisse).
    4. Nachbarschaft/Lage-Eindruck.
    Gib mir kurz und prägnant:
    - TOP 3 CHANCEN
    - TOP 3 RISIKEN
    """
    response = model.generate_content([prompt, img])
    return response.text

def main():
    st.title("☀️ Andalusien Real Estate AI-Expert")
    st.subheader("Automatischer Risiko- & Chancen-Check")

    Dateien = st.file_uploader("Objekt-Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if Dateien:
        if not api_key:
            st.warning("Bitte gib links in der Sidebar deinen API-Key ein, um die KI-Analyse zu starten.")
        
        objekt_ergebnisse = []

        for i, d in enumerate(Dateien):
            col1, col2 = st.columns([1, 1])
            img = Image.open(d)
            
            with col1:
                st.image(img, caption=f"Objekt {i+1}", use_container_width=True)
                stadt = st.text_input(f"Stadt/Lage ({i})", key=f"s_{i}")
                preis = st.number_input(f"Kaufpreis € ({i})", key=f"p_{i}")

            with col2:
                if st.button(f"🔍 KI-Analyse starten für Objekt {i+1}", key=f"btn_{i}"):
                    with st.spinner("KI untersucht das Bild..."):
                        analyse_text = analyze_image(img)
                        st.session_state[f"analysis_{i}"] = analyse_text
                
                if f"analysis_{i}" in st.session_state:
                    st.markdown("### 🤖 KI-Gutachten")
                    st.write(st.session_state[f"analysis_{i}"])
                    
                    objekt_ergebnisse.append({
                        "stadt": stadt,
                        "preis": preis,
                        "analyse": st.session_state[f"analysis_{i}"],
                        "file": d
                    })

        if objekt_ergebnisse and st.button("🚀 Profi-Report als PDF exportieren"):
            pdf = FPDF()
            for obj in objekt_ergebnisse:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"Exposé: {obj['stadt']}", ln=1)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 7, f"\nKI-ANALYSE:\n{obj['analyse']}")
                # Bild hinzufügen (vereinfacht)
                # ... (Bild-Export-Logik wie gehabt)
            
            pdf.output("Andalusien_Expert_Report.pdf")
            st.success("Dossier mit KI-Gutachten erstellt!")

if __name__ == "__main__":
    main()
