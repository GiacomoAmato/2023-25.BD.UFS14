import azure.functions as func
import logging
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

def load_html():
    try:
        html_path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        logging.error(f"Errore nel leggere il file HTML: {e}")
        return None

def load_csv():
    csv_path = os.path.join(os.path.dirname(__file__), 'GLD_data_AV_clean_no_outliers.csv')
    if not os.path.exists(csv_path):
        logging.error(f"File CSV non trovato: {csv_path}")
        return None
    df = pd.read_csv(csv_path)
    logging.info(f"Colonne trovate nel CSV: {df.columns.tolist()}")
    return df

def calculate_returns(df, frequency):
    try:
        if 'close' not in df.columns or 'date' not in df.columns:
            logging.error("Il file CSV non contiene le colonne richieste ('date' e 'close').")
            return None

        df['date'] = pd.to_datetime(df['date'])

        if frequency == 'daily':
            df['Return'] = df['close'].pct_change()
            df = df[::5]
        elif frequency == 'monthly':
            df.set_index('date', inplace=True)
            df = df.resample('M').last()
            df['Return'] = df['close'].pct_change()
        elif frequency == 'annual':
            df.set_index('date', inplace=True)
            df = df.resample('A').last()
            df['Return'] = df['close'].pct_change()
        else:
            logging.error(f"Frequenza non valida: {frequency}")
            return None
        return df
    except Exception as e:
        logging.error(f"Errore nel calcolo dei ritorni: {e}")
        return None

def generate_plot(df, frequency):
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['Return'], linestyle='-', linewidth=0.5)
        plt.title(f'Returns - {frequency.capitalize()}')
        plt.xlabel('Date')
        plt.ylabel('Returns')
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        logging.error(f"Errore durante la generazione del grafico: {e}")
        return None

@app.route(route="index.html", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    frequency = req.params.get('frequency')

    if not frequency:
        html_content = load_html()
        if html_content:
            return func.HttpResponse(html_content, status_code=200, mimetype="text/html")
        else:
            return func.HttpResponse("Si è verificato un errore nel caricare la pagina.", status_code=500)

    if frequency in ['daily', 'monthly', 'annual']:
        df = load_csv()
        if df is None:
            return func.HttpResponse("File CSV non trovato.", status_code=500)

        df_returns = calculate_returns(df, frequency)
        if df_returns is None:
            return func.HttpResponse("Errore nel calcolo dei ritorni.", status_code=500)

        plot_image = generate_plot(df_returns, frequency)
        if plot_image is None:
            return func.HttpResponse("Errore durante la generazione del grafico.", status_code=500)

        return func.HttpResponse(body=plot_image, status_code=200, mimetype="image/png")
    else:
        return func.HttpResponse("Parametro 'frequency' non valido. Utilizza 'daily', 'monthly' o 'annual'.", status_code=400)
