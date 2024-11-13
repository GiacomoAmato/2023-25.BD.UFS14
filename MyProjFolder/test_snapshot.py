import pytest
import pandas as pd
import json
from main import generate_plot
from snapshottest import Snapshot

def test_generate_plot_snapshot(snapshot):

    data = {
        'date': pd.date_range(start='2020-01-01', periods=5, freq='D'),
        'Return': [0.0, 0.05, 0.0476, 0.0455, 0.0435]
    }
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    plot_image = generate_plot(df, 'daily')
    assert plot_image is not None, "La funzione dovrebbe restituire un'immagine"

    import base64
    image_base64 = base64.b64encode(plot_image).decode('utf-8')
    snapshot.assert_match(image_base64)
