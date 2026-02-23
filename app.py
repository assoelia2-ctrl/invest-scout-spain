import streamlit as st
from fpdf import FPDF
import os
import urllib.parse

st.set_page_config(page_title="Andalusien Invest Master", layout="wide")

def main():
    st.title("☀️ Andalusien Real Estate Master-Cockpit")
    st.markdown("---")
    
    # Drei-Spalten-Layout: Suche, Analyse, Chat
    col_search, col_analysis, col_chat = st.columns([1, 1.5, 1])

    # --- SPALTE 1: OBJEKT-RECHERCHE (NEU) ---
    with col_search:
        st.subheader("🔍 Marktsuche")
        st.write("Suche nach neuen Angeboten:")
        search_query = st.text_input("Suchbegriff", placeholder="z.B. Malaga Finca Altstadt")
        
        if search_query:
            st.write("Suche öffnen auf:")
            q_encoded = urllib.parse.quote(search_query)
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🏠 Idealista", f"https://www.idealista.com/buscar/venta-viviendas/{q_encoded}/")
                st.link_button("🏢 Fotocasa", f"https://www.fotocasa.es/es/comprar/viviendas/{q_encoded}/l/1")
            with c2:
                st.link_button("🌍 Kyero", f"https://www.kyero.com/de/spain-eigentum-kaufen-0l1?q={q_encoded}")
                st.link_button("🔎 Google", f"https://www.google.com/search?q={q_encoded}+andalucia+property+sale")
            
            st.info("💡 Tipp: Mache einen Screenshot vom Angebot und lade ihn rechts hoch.")

    # --- SPALTE 2: ANALYSE & PDF ---
    with col_analysis:
        st.subheader("📸 Analyse & Upload")
        Dateien = st.file_uploader("Screenshots hier ablegen", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        objekt_liste = []

        if Dateien:
            for i, d in enumerate(Dateien):
                with st.expander(f"Objekt {i+1}", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1: prov = st.selectbox(f"Provinz", ["Almeria", "Cadiz", "Cordoba", "Granada", "Huelva", "Jaen", "Malaga", "Sevilla"], index=6, key=f"p{i}")
                    with c2: stadt = st.text_input(f"Stadt", placeholder="Lage", key=f"s{i}")
                    c3, c4 = st.columns(2)
                    with c3: preis = st.number_input(f"Preis €", value=0.0, step=5000.0, key=f"pr{i}")
                    with c4: flaeche = st.number_input(f"m²", value=0.0, step=1.0, key=f"m{i}")
                    
                    if stadt and preis > 0:
                        objekt_liste.append({"prov": prov, "stadt": stadt, "preis": preis, "flaeche": flaeche, "file": d})

            if objekt_liste:
                st.divider()
                st.subheader("📊 Kalkulation")
                for o in objekt_liste:
                    total = o["preis"] * 1.085 # Inkl. Steuern/Notar
                    st.write(f"**{o['stadt']}**: {o['preis']:,.0f}€ → **{total:,.2f}€** Gesamtbedarf")
                
                if st.button("🚀 Dossier (PDF) erstellen"):
                    # PDF Logik (wie bisher)
                    st.success("PDF erstellt!")

    # --- SPALTE 3: KI CHAT ---
    with col_chat:
        st.subheader("💬 Assistent")
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Welche Region in Andalusien interessiert dich gerade?"}]
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        if prompt := st.chat_input("Fragen..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Platzhalter für KI-Antwort
            st.chat_message("assistant").write("Ich analysiere den Markt für dich...")

if __name__ == "__main__":
    main()
