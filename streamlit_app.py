import streamlit as st
import google.generativeai as genai
import os

# Seite konfigurieren
st.set_page_config(page_title="Logik-Detektiv", page_icon="🕵️‍♂️")

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    # WICHTIG: Wir setzen die API-Version explizit auf v1 (stabil) statt v1beta
    os.environ["GOOGLE_API_VERSION"] = "v1" 
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Wir probieren das stabilste Modell-Kürzel
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Schlüssel fehlt in den Secrets! ❌")
    st.stop()

st.title("🕵️‍♂️ Der Logik-Detektiv")
st.write("Füttere mich mit deinem Plot, und ich finde die Löcher!")

# Eingabebereich
user_input = st.text_area("Beschreibe deine Szene oder deinen Plot-Punkt:", 
                          placeholder="z.B.: Der Held springt aus dem 10. Stock, landet sanft auf dem Asphalt und rennt sofort weiter...")

if st.button("Auf Logikfehler prüfen"):
    if user_input:
        with st.spinner('Der Detektiv kombiniert...'):
            try:
                prompt = f"Du bist ein Logik-Detektiv für Romanautoren. Analysiere diesen Plot auf Fehler: {user_input}"
                response = model.generate_content(prompt)
                
                st.subheader("Analyse-Ergebnis:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Schnittstellen-Fehler: {e}")
                st.write("Tipp: Falls wieder 404 erscheint, versuche 'gemini-pro' statt 'gemini-1.5-flash' im Code.")
    else:
        st.warning("Bitte gib erst einen Text ein!")