import requests
import pandas as pd

def avget_data(stock, key):
    """
    Lädt die Zeitreihendaten der Aktie als json-Datei herunter (Funktion TIME_SERIES_DAILY)
    Rückgabe als json
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def avget_dates(data):
    """
    Filtert die Datierung der Daten aus der TIME_SERIES_DAILY Funktion der API
    Rückgabe als Liste
    """
    dates = []
    for date in data['Time Series (Daily)']:
        dates.append(date)
    return dates

def avget_prices(data):
    """
    Filtert die Closing-Preise der Daten aus der TIME_SERIES_DAILY Funktion der API
    Rückgabe als Liste
    """
    prices = []
    for date in data['Time Series (Daily)']:
        price = float(data['Time Series (Daily)'][date]['4. close'])
        prices.append(price)
    return prices

def avget_df(dates, prices):
    """
    Kombiniert Daten und Preise in ein Dataframe (vereinfacht Plot mit Plotly)
    """
    df = pd.DataFrame({
        "Datum": dates,
        "Kurs in $": prices,
    })
    return df

def avget_search(keyword, key):
    """
    Fragt die Funktion SYMBOL_SEARCH der API ab, welche wie eine Suchmaschine für Aktien Symbole funktioniert.
    Rückgabe als json
    """
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def avget_matches(searchdata):
    """
    Filtert die Namen der Unternehmen und zugehörigen Symbole aus der SYMBOL_SEARCH Funktion der API.
    Rückgabe als Liste im Schema Symbol - Name des Unternehmens
    """
    matches = []
    for match in searchdata['bestMatches']:
        symbol = match['1. symbol']
        name = match['2. name']
        matches.append(f"{symbol} - {name}")
    return matches

