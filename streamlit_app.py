import streamlit as st
import google.generativeai as genai
import os

# Seite konfigurieren
st.set_page_config(page_title="Logik-Detektiv", page_icon="🕵️‍♂️")

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    # Wir erzwingen die stabilste Version
    os.environ["GOOGLE_API_VERSION"] = "v1" 
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # WECHSEL: Wir nutzen 'gemini-pro', das ist am kompatibelsten
    try:
        model = genai.GenerativeModel('gemini-pro')
    except Exception:
        # Falls selbst das nicht geht, versuchen wir die absolute Basis-Variante
        model = genai.GenerativeModel('models/gemini-pro')
else:
    st.error("Schlüssel fehlt in den Secrets! ❌")
    st.stop()

st.title("🕵️‍♂️ Der Logik-Detektiv")
st.write("Füttere mich mit deinem Plot, und ich finde die Löcher!")

# Eingabebereich
user_input = st.text_area("Beschreibe deine Szene oder deinen Plot-Punkt:", 
                          placeholder="z.B.: Die Figur sieht im Dunkeln eine rote Krawatte...")

if st.button("Auf Logikfehler prüfen"):
    if user_input:
        with st.spinner('Der Detektiv kombiniert...'):
            try:
                # Wir halten den Prompt simpel für den ersten Erfolgstest
                prompt = f"Prüfe diesen Text auf Logikfehler: {user_input}"
                response = model.generate_content(prompt)
                
                st.subheader("Analyse-Ergebnis:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Fehler bei der Anfrage: {e}")
                st.write("Hinweis: Überprüfe, ob dein API-Key in der secrets.toml wirklich korrekt ist.")
    else:
        st.warning("Bitte gib erst einen Text ein!")