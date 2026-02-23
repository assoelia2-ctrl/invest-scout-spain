import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
import os
from PIL import Image

# --- KONFIGURATION ---
st.set_page_config(page_title="Andalusien AI Expert Pro", layout="wide")

# Sidebar für Einstellungen
with st.sidebar:
    st.header("⚙️ Einstellungen")
    api_key = st.text_input("Gemini API Key eingeben", type="password")
    st.info("Den Key erhältst du kostenlos im Google AI Studio.")

# KI-Modell initialisieren
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_image(img):
    """Der spezialisierte Analyse-Prompt für andalusische Immobilien"""
    prompt = """
    Du bist ein zertifizierter Baugutachter für Immobilien in Andalusien (Spanien). 
    Analysiere diesen Screenshot technisch und investitionsorientiert nach folgenden Kriterien:

    1. SUBSTANZ-CHECK: 
       - Achte auf Feuchtigkeitsränder an Fassaden (Salpeter/Humedad). 
       - Prüfe den Zustand der Dachziegel (Tejas) und Regenrinnen.
       - Sind statische Risse über Fenstern oder an Gebäudeecken erkennbar?

    2. TOPOGRAPHIE & ZUFAHRT:
       - Ist der Weg 'asfaltado' (asphaltiert) oder ein 'carril' (Feldweg)? 
       - Schätze die Steigung der Zufahrt (Befahrbarkeit für LKW/Baustellenfahrzeuge).
       - Vegetation: Erkennst du geschützte Bäume wie Oliven oder Korkeichen im Baufeld?

    3. SCHATTEN & ENERGIE:
       - Analysiere den Schattenwurf von Nachbargebäuden oder Bergen (Nordhang-Risiko?).
       - Schätze die nutzbare Dachfläche für Photovoltaik (Süd-Ausrichtung).

    4. INFRASTRUKTUR:
       - Siehst du Strommasten, Wassertanks (Depósitos) oder Glasfaser-Anschlüsse?

    Gliedere deine Antwort strikt und übersichtlich in:
    - 🚩 RISIKEN (Baulich, Lage & Rechtlich)
    - ✨ CHANCEN (Aufwertungspotenzial & Cashflow)
    - 💶 SCHÄTZUNG (Grobe Richtung für sofortige Instandsetzungskosten)
    """
    response = model.generate_content([prompt, img])
    return response.text

def main():
    st.title("☀️ Andalusien Real Estate AI-Expert")
    st.write("Dein digitaler Gutachter für den spanischen Immobilienmarkt.")

    # Datei-Upload
    Dateien = st.file_uploader("Objekt-Screenshots hochladen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if Dateien:
        if not api_key:
            st.error("❌ Bitte gib zuerst deinen API-Key in der Sidebar ein!")
            return
        
        objekt_ergebnisse = []

        for i, d in enumerate(Dateien):
            st.markdown(f"---")
            col1, col2 = st.columns([1, 1.2])
            
            img = Image.open(d)
            
            with col1:
                st.image(img, caption=f"Original Screenshot {i+1}", use_container_width=True)
                stadt = st.text_input(f"Stadt / Region", key=f"stadt_{i}", placeholder="z.B. Nerja,
