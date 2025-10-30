# core/importer/layouts.py

TORRE_X = {
    "name": "Torre X",
    "columns": {
        # 🕓 Tempo
        "Date/time": "datetime",

        # 🌬️ Anemômetro (2m)
        "Anemômetro;wind_speed;Avg": "Spd_2m",
        "Anemômetro;wind_speed;Max": "Spd_2m_Max",
        "Anemômetro;wind_speed;Min": "Spd_2m_Min",
        "Anemômetro;wind_speed;StdDev": "Spd_2m_SD",
        "Anemômetro;wind_speed;Count": "Spd_2m_Count",

        # 💧 Umidade relativa
        "TH;humidity;Avg": "Hum_Avg",
        "TH;humidity;Max": "Hum_Max",
        "TH;humidity;Min": "Hum_Min",
        "TH;humidity;StdDev": "Hum_SD",
        "TH;humidity;Count": "Hum_Count",

        # 🌡️ Temperatura do ar
        "TH;temperature;Avg": "Temp_Avg",
        "TH;temperature;Max": "Temp_Max",
        "TH;temperature;Min": "Temp_Min",
        "TH;temperature;StdDev": "Temp_SD",
        "TH;temperature;Count": "Temp_Count",

        # ☀️ Piranômetros (radiação solar)
        "Piranômetro 1;solar_irradiance;Avg": "Rad1_Avg",
        "Piranômetro 1;solar_irradiance;Max": "Rad1_Max",
        "Piranômetro 1;solar_irradiance;Min": "Rad1_Min",
        "Piranômetro 1;solar_irradiance;StdDev": "Rad1_SD",
        "Piranômetro 1;solar_irradiance;Count": "Rad1_Count",

        "Piranômetro 2;solar_irradiance;Avg": "Rad2_Avg",
        "Piranômetro 2;solar_irradiance;Max": "Rad2_Max",
        "Piranômetro 2;solar_irradiance;Min": "Rad2_Min",
        "Piranômetro 2;solar_irradiance;StdDev": "Rad2_SD",
        "Piranômetro 2;solar_irradiance;Count": "Rad2_Count",

        "Piranômetro 3;solar_irradiance;Avg": "Rad3_Avg",
        "Piranômetro 3;solar_irradiance;Max": "Rad3_Max",
        "Piranômetro 3;solar_irradiance;Min": "Rad3_Min",
        "Piranômetro 3;solar_irradiance;StdDev": "Rad3_SD",
        "Piranômetro 3;solar_irradiance;Count": "Rad3_Count",

        # 🌧️ Pluviômetro
        "Pluviômetro;precipitation;Count": "Rain_Count",
        "Pluviômetro;precipitation;Sum": "Rain_Sum",

        # ☀️ Albedo
        "Albedo;albedo;Avg": "Albedo_Avg",
        "Albedo;albedo;Max": "Albedo_Max",
        "Albedo;albedo;Min": "Albedo_Min",
        "Albedo;albedo;StdDev": "Albedo_SD",
        "Albedo;albedo;Count": "Albedo_Count",

        # 📈 Sensores A1–A5 (auxiliares)
        "A1;Avg": "A1_Avg",
        "A1;Max": "A1_Max",
        "A1;Min": "A1_Min",
        "A1;StdDev": "A1_SD",
        "A1;Count": "A1_Count",

        "A2;Avg": "A2_Avg",
        "A2;Max": "A2_Max",
        "A2;Min": "A2_Min",
        "A2;StdDev": "A2_SD",
        "A2;Count": "A2_Count",

        "A3;Avg": "A3_Avg",
        "A3;Max": "A3_Max",
        "A3;Min": "A3_Min",
        "A3;StdDev": "A3_SD",
        "A3;Count": "A3_Count",

        "A4;Avg": "A4_Avg",
        "A4;Max": "A4_Max",
        "A4;Min": "A4_Min",
        "A4;StdDev": "A4_SD",
        "A4;Count": "A4_Count",

        "A5;Avg": "A5_Avg",
        "A5;Max": "A5_Max",
        "A5;Min": "A5_Min",
        "A5;StdDev": "A5_SD",
        "A5;Count": "A5_Count",

        # 🌡️ Canais C1 e C2
        "C1;Avg": "C1_Avg",
        "C1;Max": "C1_Max",
        "C1;Min": "C1_Min",
        "C1;StdDev": "C1_SD",
        "C1;Count": "C1_Count",

        "C2;Avg": "C2_Avg",
        "C2;Max": "C2_Max",
        "C2;Min": "C2_Min",
        "C2;StdDev": "C2_SD",
        "C2;Count": "C2_Count",

        # ⚡ Tensão, Corrente e Temperatura interna
        "V;Avg": "V_Avg",
        "V;Max": "V_Max",
        "V;Min": "V_Min",

        "I;Avg": "I_Avg",
        "I;Max": "I_Max",
        "I;Min": "I_Min",

        "T;Avg": "T_Avg",

        # Endereço ou ID
        "addr": "Address",
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
    },
}

LAYOUTS = {
    "Torre X": TORRE_X,
    "Torre Y": TORRE_Y,
}
