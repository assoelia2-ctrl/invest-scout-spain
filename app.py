import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# ... (Dein bisheriger Setup-Code mit API Key) ...

# NEU: Verbesserte Agenten-Anweisung für präzisere Vergleiche
def agent_call_pro(prompt, image=None):
    model = genai.GenerativeModel('gemini-1.5-pro') # Pro-Modell für tiefere Analysen
    
    system_instruction = """
    Du bist ein Elite-Immobilien-Agent in Spanien. 
    1. Wenn ein Bild hochgeladen wird, identifiziere den Ort, Baustil und Zustand.
    2. Suche im Internet nach Vergleichswerten für diesen Standort.
    3. Erstelle eine Tabelle mit: Preis, geschätzter Rendite und Investment-Risiko (1-10).
    4. Gib eine klare 'Kauf'- oder 'Warten'-Empfehlung.
    """
    
    full_prompt = f"{system_instruction}\n\nUser-Anfrage: {prompt}"
    
    inputs = [full_prompt]
    if image:
        inputs.append(image)
    
    response = model.generate_content(inputs)
    return response.text

# --- ERWEITERTES UI ---
with st.sidebar:
    st.header("⚙️ Agenten-Tuning")
    st.slider("Risiko-Toleranz", 1, 10, 5)
    st.checkbox("Nebenkosten einrechnen (ITP/IVA)", value=True)
    st.markdown("---")
    if st.button("Analyse als PDF exportieren"):
        st.toast("PDF wird generiert... (Funktion in Vorbereitung)")

# (Der Rest bleibt wie in deiner app.py, aber wir nutzen agent_call_pro)
