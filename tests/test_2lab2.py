import pandas as pd
import pytest
from dtw_lab.lab1 import encode_categorical_vars

def test_encode_categorical_vars_basic():
    df = pd.DataFrame({
        "Battery_Size": ["AAA", "AA", "C", "D"],
        "Discharge_Speed": ["Slow", "Medium", "Fast", "Medium"],
        "Manufacturer": ["Sony", "Panasonic", "Duracell", "Energizer"]
    })

    df_encoded = encode_categorical_vars(df)

    # Comprobamos mapeo de Battery_Size
    assert list(df_encoded["Battery_Size"]) == [1, 2, 3, 4]

    # Comprobamos mapeo de Discharge_Speed
    assert list(df_encoded["Discharge_Speed"]) == [1, 2, 3, 2]

    # Comprobamos creación de columnas dummies de Manufacturer
    for manufacturer in ["Manufacturer_Duracell", "Manufacturer_Energizer", "Manufacturer_Panasonic", "Manufacturer_Sony"]:
        assert manufacturer in df_encoded.columns

def test_encode_categorical_vars_missing_and_duplicates():
    df = pd.DataFrame({
        "Battery_Size": ["AAA", "AA", "AA", "D"],
        "Discharge_Speed": ["Slow", "Fast", "Fast", "Medium"],
        "Manufacturer": ["Sony", "Sony", "Duracell", "Duracell"]
    })

    df_encoded = encode_categorical_vars(df)

    # Valores mapeados de Battery_Size y Discharge_Speed
    assert list(df_encoded["Battery_Size"]) == [1, 2, 2, 4]
    assert list(df_encoded["Discharge_Speed"]) == [1, 3, 3, 2]

    # Columnas dummies de Manufacturer
    for manufacturer in ["Manufacturer_Duracell", "Manufacturer_Sony"]:
        assert manufacturer in df_encoded.columns