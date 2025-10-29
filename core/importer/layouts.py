# core/importer/layouts.py

TORRE_X = {
    "name": "Torre X",
    "columns": {
        "Date/time": "datetime",
        
        "Anemômetro;wind_speed;Avg": "wind_avg",
        "Anemômetro;wind_speed;Max": "wind_max",
        "Anemômetro;wind_speed;Min": "wind_min",
        "Anemômetro;wind_speed;StdDev": "wind_std",
        "TH;humidity;Avg": "humidity_avg",
        "TH;humidity;Max": "humidity_max",
        "TH;humidity;Min": "humidity_min",
        "TH;humidity;StdDev": "humidity_std",
        "TH;temperature;Avg": "temperature_avg",
        "TH;temperature;Max": "temperature_max",
        "TH;temperature;Min": "temperature_min",
    },
}

TORRE_Y = {
    "name": "Torre Y",
    "columns": {
        "DataHora": "datetime",
        "VelocidadeMedia": "wind_avg",
        "VelocidadeMaxima": "wind_max",
        "Temperatura": "temperature_avg",
        "Umidade": "humidity_avg",
    }
}

LAYOUTS = {
    "Torre X": TORRE_X,
    "Torre Y": TORRE_Y,
}
