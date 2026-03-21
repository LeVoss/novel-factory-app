import streamlit as st
import google.generativeai as genai
import os
# Verbindung zum "Tresor" herstellen
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Das Gehirn der Novel Factory
st.set_page_config(page_title="The Novel Factory - Logik-Detektiv", layout="centered")

st.title("🕵️‍♂️ Der Logik-Detektiv")
st.subheader("Finde Plot-Löcher, bevor es deine Leser tun.")

# Dein Experten-Prompt (Das Herzstück)
LOGIK_PROMPT = """
Du bist der Logik-Detektiv der Novel Factory. Analysiere den folgenden Text streng auf:
- Widersprüche im Wissen der Charaktere.
- Zeitliche Unstimmigkeiten.
- Fehler bei Objekten oder dem Ort des Geschehens.
Gib die Fehler in einer Liste aus und mache einen konkreten Vorschlag zur Korrektur.
Wenn alles logisch ist, lobe den Autor kurz.
"""

text_input = st.text_area("Füge hier deine Szene ein:", height=300, placeholder="Kapitel 1: Der Kommissar betritt den Raum...")

if st.button("Logik-Check starten"):
    if text_input:
        with st.spinner('Analysiere Plot-Struktur...'):
            # Hier wird später deine KI-Verbindung (API-Key) eingefügt
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{LOGIK_PROMPT}\n\nText:\n{text_input}")
            st.markdown("### 📋 Analyse-Bericht:")
            st.write(response.text)
    else:
        st.warning("Bitte gib zuerst einen Text ein.")
