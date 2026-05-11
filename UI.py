from API_AlphaVantage import avget_data, avget_df, avget_prices, avget_dates, avget_search, avget_matches
from API_AI import ai_getanalysis
import streamlit as st
import plotly.express as px

av_key = st.secrets["ALPHAVANTAGE_KEY"]
mammouth_key = st.secrets["MAMMOUTH_KEY"]


# Überschrift

st.set_page_config(page_title="Aktien-Dashboard", page_icon="📈", layout="wide")
st.title("📈 Aktien-Dashboard")

st.divider()


# Suchleiste

col1, col2 = st.columns([3, 1]) # Spalten für Suchfeld und Suchbutton

with col1:
    search_query = st.text_input("Aktien-Symbol oder Name", "Apple", label_visibility="collapsed")

with col2:
    search_clicked = st.button("Suchen", use_container_width=True)

if search_clicked: # Wenn gesucht wird: API anfragen und Suchergebnisse im Session State ("Cache") speichern
    if search_query:
        with st.spinner("Suche..."):
            st.session_state["suggestions"] = avget_matches(avget_search(search_query, av_key))

            if not st.session_state["suggestions"]:
                st.warning("Keine Treffer gefunden oder API-Limit erreicht.")
    else:
        st.warning("Bitte gib einen Suchbegriff ein.")


# Auswahlfeld & Abruf-Button

stock_to_fetch = ""
selected_option = ""

st.write("Wähle den passenden Treffer aus und rufe die Daten ab:")

col3, col4 = st.columns([3, 1]) # Spalten für Auswahlfeld und Abruf-Button

with col3:
    if "suggestions" in st.session_state and st.session_state["suggestions"]: # Prüfung ob Liste vorhanden und ob diese nicht leer ist
        selected_option = st.selectbox(
            "Wähle den passenden Treffer:",
            st.session_state["suggestions"],
            label_visibility="collapsed" # Versteckt das Label
        )
        stock_to_fetch = selected_option.split(" - ")[0] # Aus z.B. "AAPL - Apple Inc." wird "AAPL"
    else:
        stock_to_fetch = search_query # Wenn noch nicht gesucht wurde
        st.info(f"Aktuelles Symbol: **{stock_to_fetch}**")

with col4:
    fetch_clicked = st.button("Daten abrufen", use_container_width=True) # Button um Daten abzurufen

st.divider()


# Datenabruf & Plot

if fetch_clicked:
    if not stock_to_fetch:
        st.error("Bitte wähle zuerst eine Aktie aus.")
    else:
        with st.spinner(f"Lade Kursdaten für {stock_to_fetch}..."):
            avdata = avget_data(stock_to_fetch, av_key) # API aufrufen
            df = avget_df(avget_dates(avdata), avget_prices(avdata)) # In DataFrame umwandeln für Plot

            if df is not None and not df.empty: # Plotten wenn das DataFrame Daten enthält
                st.subheader(f"Kursdaten für: {stock_to_fetch}")
                current_price = df["Kurs in $"].iloc[0]
                previous_price = df["Kurs in $"].iloc[1]
                delta_value = current_price - previous_price # Berechnung der Tagesdifferenz (Wert)
                delta_percent = (delta_value / previous_price) * 100 # Berechnung der Tagesdifferenz (Prozent)

                st.metric(label=f"Letzter Kurs", value=f"{current_price:.2f} $", delta=f"{delta_value:.2f} $ | {delta_percent:.2f} %")

                fig = px.line( # Plot erstellen
                    df,
                    x="Datum",
                    y="Kurs in $",
                    markers=True,
                    title=f"Kursverlauf"
                )
                fig.update_layout(xaxis_title="Datum", yaxis_title="Preis in $")
                st.plotly_chart(fig, use_container_width=True) # Plot in Streamlit zeigen

                analysis = ai_getanalysis(selected_option, mammouth_key) # Perplexity API aufrufen
                with st.container(border=True):
                    st.markdown(f"**Aktuelle Marktlage:**\n> {analysis}") # Die Zusammenfassung darstellen

            else:
                st.error("Es konnten keine Daten geladen werden. Möglicherweise ist das API-Limit (25 Anfragen/Tag) erreicht.")

            st.divider()


            # Rohdaten & Beispiel

            with st.expander("Rohdaten (json)"):
                st.json(avdata)

json_snippet = """{
  "id": "chatcmpl-123456789",
  "object": "chat.completion",
  "created": 1715432100,
  "model": "sonar-pro",
  "usage": {
    "prompt_tokens": 145,
    "completion_tokens": 56,
    "total_tokens": 201
  },
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Apple hat kürzlich starke Quartalszahlen vorgelegt... Empfehlung: Kaufen 🟢"
      },
      "finish_reason": "stop"
    }
  ]
}"""

with st.expander("KI API Antwort (Beispiel)"):
    st.code(json_snippet, language="json", line_numbers=True)