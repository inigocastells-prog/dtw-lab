import pandas as pd
from dtw_lab.lab1 import encode_categorical_vars
from dtw_lab.lab1 import calculate_statistic

def test_calculate_statistic():
    df = pd.DataFrame({"Charge_Left_Percentage": [39, 60, 30, 30, 41]})
    assert calculate_statistic("mean", df["Charge_Left_Percentage"]) == 40
    assert calculate_statistic("median", df["Charge_Left_Percentage"]) == 39
    assert calculate_statistic("mode", df["Charge_Left_Percentage"]) == 30

def test_encode_categorical_vars():
    df = pd.DataFrame(
        {
            "Manufacturer": ["A", "B"],
            "Battery_Size": ["AA", "AAA"],
            "Discharge_Speed": ["Slow", "Fast"],
        }
    )

    encoded = encode_categorical_vars(df)

    assert "Manufacturer_A" in encoded.columns
    assert "Manufacturer_B" in encoded.columns
    assert encoded["Battery_Size"].iloc[0] == 2
    assert encoded["Battery_Size"].iloc[1] == 1
    assert encoded["Discharge_Speed"].iloc[0] == 1
    assert encoded["Discharge_Speed"].iloc[1] == 3


