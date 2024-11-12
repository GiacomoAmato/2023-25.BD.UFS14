import azure.functions as func
import logging
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

# Inizializza l'app Azure Functions
app = func.FunctionApp()

@app.route(route="index.html", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Recupera il parametro 'frequency' dalla richiesta
    frequency = req.params.get('frequency')
    if not frequency:
        try:
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
        try:
            csv_path = os.path.join(os.path.dirname(__file__), 'GLD_data_AV_clean_no_outliers.csv')
            if not os.path.exists(csv_path):
                logging.error(f"File CSV non trovato: {csv_path}")
                return func.HttpResponse("File CSV non trovato.", status_code=500)
                
            df = pd.read_csv(csv_path)

            logging.info(f"Colonne trovate nel CSV: {df.columns.tolist()}")
            if 'close' not in df.columns or 'date' not in df.columns:
                logging.error("Il file CSV non contiene le colonne richieste ('date' e 'close').")
                return func.HttpResponse("Il file CSV non contiene le colonne richieste ('date' e 'close').", status_code=500)

            # Calcolo dei ritorni in base alla frequenza
            if frequency == 'daily':
                df['Return'] = df['close'].pct_change()
                # Prendi solo ogni 5 giorni per ridurre il numero di punti
                df = df[::5]
            elif frequency == 'monthly':
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                df = df.resample('M').last()
                df['Return'] = df['close'].pct_change()
            elif frequency == 'annual':
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                df = df.resample('A').last()
                df['Return'] = df['close'].pct_change()

            # Genera il grafico dei ritorni
            plt.figure(figsize=(10, 5))
            plt.plot(df.index, df['Return'],  linestyle='-', linewidth=0.5)
            plt.title(f'Returns - {frequency.capitalize()}')
            plt.xlabel('Date')
            plt.ylabel('Returns')
            plt.grid()

            # Migliora la leggibilità delle date sull'asse x
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Salva il grafico in un buffer di memoria
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)

            return func.HttpResponse(
                body=buf.getvalue(),
                status_code=200,
                mimetype="image/png"
            )
        except Exception as e:
            logging.error(f"Errore durante il calcolo o la generazione del grafico: {e}")
            return func.HttpResponse(
                "Si è verificato un errore durante l'elaborazione della richiesta.",
                status_code=500
            )
    else:
        return func.HttpResponse(
            "Parametro 'frequency' non valido. Utilizza 'daily', 'monthly' o 'annual'.",
            status_code=400
        )
