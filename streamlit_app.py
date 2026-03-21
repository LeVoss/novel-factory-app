import streamlit as st
import google.generativeai as genai

# Seite konfigurieren
st.set_page_config(page_title="Logik-Detektiv", page_icon="🕵️‍♂️")

# Verbindung zum Key herstellen
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # AUTOMATIK: Wir holen uns die Liste der erlaubten Modelle
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            # Wir nehmen das erste Modell aus deiner Liste
            selected_model = available_models[0]
            model = genai.GenerativeModel(selected_model)
        else:
            st.error("Keine passenden Modelle gefunden.")
            st.stop()
    except Exception as e:
        st.error(f"Fehler beim Laden der Modelle: {e}")
        st.stop()
else:
    st.error("Schlüssel fehlt in den Secrets! ❌")
    st.stop()

st.title("🕵️‍♂️ Der Logik-Detektiv")
st.write(f"Aktiviertes Modell: `{selected_model}`") # Zeigt dir an, was er nutzt

# Eingabebereich
user_input = st.text_area("Beschreibe deine Szene oder deinen Plot-Punkt:", 
                          placeholder="z.B.: Er schloss die Tür von außen ab, obwohl er noch im Zimmer stand...")

if st.button("Auf Logikfehler prüfen"):
    if user_input:
        with st.spinner('Der Detektiv kombiniert...'):
            try:
                prompt = f"Analysiere diesen Roman-Plot auf Logikfehler oder unrealistische Abläufe: {user_input}"
                response = model.generate_content(prompt)
                
                st.subheader("Analyse-Ergebnis:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Analyse fehlgeschlagen: {e}")
    else:
        st.warning("Bitte gib erst einen Text ein!")