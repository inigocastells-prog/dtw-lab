# tests/test_lab2_statistic.py
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from dtw_lab.lab2 import app

client = TestClient(app)

def test_get_statistic_mean(mocker):
    # Fake DataFrame with all required columns for clean_data
    fake_df = pd.DataFrame({
        "Avg_Operating_Temperature": [20, 30, 40, 50, 60],
        "Charge_Left_Percentage": [50, 60, 70, 80, 90],
        "Current_Voltage": [1, 1, 1, 1, 1],
        "Days_Since_Production": [100, 200, 300, 400, 500],
        "Battery_Size": ['AA', 'AA', 'AA', 'AA', 'AA']
    })

    # IMPORTANTE: Parchear donde se USAN las funciones (lab2), no donde se definen (lab1)
    mocker.patch('dtw_lab.lab2.read_csv_from_google_drive', return_value=fake_df)
    mocker.patch('dtw_lab.lab2.clean_data', side_effect=lambda x: x)

    # Call the API endpoint
    response = client.get("/statistic/mean/Avg_Operating_Temperature")
    
    assert response.status_code == 200
    data = response.json()
    assert data["measure"] == "mean"
    assert data["column"] == "Avg_Operating_Temperature"
    # El promedio de [20, 30, 40, 50, 60] es 40.0
    assert float(data["value"]) == 40.0

def test_get_statistic_mode(mocker):
    # Fake DataFrame with all required columns for clean_data
    # Usamos valores que den una moda clara
    fake_df = pd.DataFrame({
        "Charge_Left_Percentage": [30, 30, 30, 60, 60],
        "Avg_Operating_Temperature": [20, 30, 40, 50, 60],
        "Current_Voltage": [1, 1, 1, 1, 1],
        "Days_Since_Production": [100, 200, 300, 400, 500],
        "Battery_Size": ['AA', 'AA', 'AA', 'AA', 'AA']
    })

    # Parchear las referencias en lab2
    mocker.patch('dtw_lab.lab2.read_csv_from_google_drive', return_value=fake_df)
    mocker.patch('dtw_lab.lab2.clean_data', side_effect=lambda x: x)

    # Call the API endpoint
    response = client.get("/statistic/mode/Charge_Left_Percentage")

    assert response.status_code == 200
    data = response.json()
    assert data["measure"] == "mode"
    assert data["column"] == "Charge_Left_Percentage"
    # La moda de [30, 30, 30, 60, 60] es 30
    assert int(data["value"]) == 30