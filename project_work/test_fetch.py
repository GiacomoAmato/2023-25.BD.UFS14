import pytest
import os
from main import fetch_ingredient_data, find_and_extract_report
import json
url = "https://cir-reports.cir-safety.org/"
'''
def test_fetch_ingredient_data():
    result = fetch_ingredient_data(url)
    assert len(result)>7000
'''

def save_snapshot(filename, content):
    """Salva il contenuto di uno snapshot."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def load_snapshot(filename):
    """Carica il contenuto di uno snapshot salvato."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def test_find_and_extract_report():
    """Test per verificare l'estrazione del report PDF di un ingrediente."""
    ingredienti = fetch_ingredient_data(url)
   
    # Selezioniamo il nome di un ingrediente specifico esistente nei dati
    ingrediente_richiesto = ingredienti[0]["pcpc_ingredientname"]
    pdf_link = find_and_extract_report(ingredienti, ingrediente_richiesto, url)
    
    snapshot_file = "ingrediente.json"
    expected_ingrediente = load_snapshot(snapshot_file)

    assert ingrediente_richiesto == expected_ingrediente, (
        f"L'ingrediente richiesto non corrisponde allo snapshot salvato! "
        f"Atteso: {expected_ingrediente}, Ottenuto: {ingrediente_richiesto}"
        )

    # Verificare che il link del PDF non sia vuoto
    assert pdf_link is not None, f"Link PDF non trovato per l'ingrediente {ingrediente_richiesto}"
    assert pdf_link.startswith("https://"), "Il link del PDF non è valido!"



