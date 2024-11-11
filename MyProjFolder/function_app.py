import azure.functions as func
import logging
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = func.FunctionApp()

@app.route(route="index.html", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    frequency = req.params.get('frequency')
    if not frequency:
        try:
            # Leggi il file HTML
            html_path = os.path.join(os.path.dirname(__file__), 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return func.HttpResponse(
                html_content,
                status_code=200,
                mimetype="text/html"
            )
        except Exception as e:
            logging.error(f"Errore nel leggere il file HTML: {e}")
            return func.HttpResponse(
                "Si è verificato un errore nel caricare la pagina.",
                status_code=500
            )

    if frequency in ['daily', 'monthly', 'annual']:
        # Il resto del tuo codice per generare il grafico
        # ...
        # Assicurati di aggiornare il percorso del file CSV se necessario
        df = pd.read_csv('GLD_data_AV_clean_no_outliers.csv')
        # (Il codice rimane lo stesso)
        # ...

        # Restituisci l'immagine come risposta
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return func.HttpResponse(
            body=buf.getvalue(),
            status_code=200,
            mimetype="image/png"
        )
    else:
        return func.HttpResponse(
            "Parametro 'frequency' non valido. Utilizza 'daily', 'monthly' o 'annual'.",
            status_code=400
        )
