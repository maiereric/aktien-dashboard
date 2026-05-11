import requests

def ai_getanalysis(symbol, api_key):
    """
    Ruft die KI-API auf und fragt eine aktuelle Zusammenfassung der Marktlage per Promt an.
    Die Chatantwort wird herausgefiltert und als String zurückgegeben
    """
    url = "https://api.mammouth.ai/v1/chat/completions" # Endpunkt für Chatantworten (completions)

    headers = { # Zusatzinfos für den Datenaustausch per requests
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Analysiere die aktuellsten Nachrichten und Analystenbewertungen zu dem US-Börsen-Ticker '{symbol}'. "
        f"WICHTIG: '{symbol}' ist zwingend ein offizielles Ticker-Kürzel einer an der NYSE oder NASDAQ gelisteten Aktie "
        f"(z.B. steht 'DE' für das US-Unternehmen Deere & Company, NICHT für Deutschland oder eine deutsche Firma!). "
        f"Leite aus dem Ticker zuerst das korrekte US-Unternehmen ab und recherchiere nur dazu. "
        f"Nenne absolut keine aktuellen Aktienkurse, Prozentangaben oder historische Kursdaten. "
        f"Verfasse eine zusammenhängende Zusammenfassung (ausschließlich Fließtext, absolut KEINE Stichpunkte!). "
        f"Antworte in maximal 3 bis 4 prägnanten, gut lesbaren Sätzen auf Deutsch. "
        f"Schließe den Text am Ende zwingend mit EXAKT einer dieser drei Schreibweisen ab: "
        f"'Empfehlung: Kaufen 🟢', 'Empfehlung: Halten 🟡' oder 'Empfehlung: Verkaufen 🔴'."
    )

    data = {
        "model": "gemini-3.1-flash-lite-preview", # Modellauswahl Google Gemini Flash, da gute Aktualität und wenig Halluzination, schnell und günstig
        "messages": [
            {
                "role": "system", # Persönlichkeit des LLMs
                "content": "Du bist ein professioneller Finanzanalyst für ein Magazin. Du schreibst elegante, zusammenhängende Fließtexte und lieferst klare Kaufempfehlungen basierend auf Nachrichten."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = None # Definition, damit response für except auf jeden Fall existiert

    try:
        response = requests.post(url, headers=headers, json=data) # hochladen des Datenpakets
        response.raise_for_status() # Prüfen auf Error
        return response.json()["choices"][0]["message"]["content"] # Rückgabe der Chatantwort

    except requests.exceptions.RequestException as e:
        return f"Fehler bei der Verbindung zur Mammouth API: {e}" # verhindert Absturz bei Verbindungsfehlern
    except (KeyError, IndexError):
        return f"Fehler beim Auslesen der Daten: {response.text}" # verhindert Absturz bei Auslesefehlern
