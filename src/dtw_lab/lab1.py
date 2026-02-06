import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import requests
from typing import Literal, Union

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the input DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame to be cleaned.
    Returns:
        pd.DataFrame: The cleaned and preprocessed DataFrame.
    """
    return df

def read_csv_from_google_drive(file_id: str) -> pd.DataFrame:
    """
    Read a CSV file from Google Drive into a pandas DataFrame.
    Args:
        file_id (str): The file ID of the CSV file in Google Drive.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the CSV data.
    Raises:
        ValueError: If the file cannot be accessed or read.
    """
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    try:
        s = requests.get(download_url).content   
        return pd.read_csv(io.StringIO(s.decode('utf-8')))
    except Exception as e:
        raise ValueError(f"Unable to read CSV file from Google Drive: {str(e)}")


def visualize_data(df: pd.DataFrame) -> None:
    """
    Visualizes relationships between various features and the 'Charge_Left_Percentage' in the given DataFrame.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing at least the following columns:
            - 'Battery_Size': Categorical data representing the size of the battery.
            - 'Discharge_Speed': Categorical data representing the speed of discharge.
            - 'Manufacturer': Categorical data representing the manufacturer of the battery.
            - 'Days_Since_Production': Numerical data representing the number of days since production.
            - 'Avg_Operating_Temperature': Numerical data representing the average operating temperature.
            - 'Current_Voltage': Numerical data representing the current voltage.
            - 'Charge_Left_Percentage': Numerical data representing the percentage of charge left.

    Returns:
        None: Displays a grid of plots visualizing the relationships between the features and 'Charge_Left_Percentage'.
    """
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    features = ['Avg_Operating_Temperature','Days_Since_Production', 'Current_Voltage']
    target_variable = 'Charge_Left_Percentage'
    for i, feature in enumerate(features):
        sns.scatterplot(data=df, x=feature, y=target_variable, ax=axs[i])
        axs[i].set_title(f'Scatter plot of {feature} vs Charge_Left_Percentage')
    plt.tight_layout()
    plt.savefig('graphs/scatter_plots.png')

    features = ['Avg_Operating_Temperature','Days_Since_Production', 'Current_Voltage']
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    for i, feature in enumerate(features):
        sns.boxplot(data=df, x=feature, ax=axs[i])
        axs[i].set_title(f'Box plot of {feature} vs Charge_Left_Percentage')
    plt.tight_layout()
    plt.savefig('graphs/boxplots.png')

    ## do the same with frequency histograms
    features = ['Battery_Size', 'Discharge_Speed', 'Manufacturer']
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    for i, feature in enumerate(features):
        sns.histplot(data=df, x=feature, ax=axs[i])
        axs[i].set_title(f'Frequency histogram of {feature}')
    plt.tight_layout()
    plt.savefig('graphs/histograms.png')



def encode_categorical_vars(df: pd.DataFrame) -> pd.DataFrame:
    #One hot encode manufacturer
    df = pd.get_dummies(df, columns=['Manufacturer'])

    #Map battery size to integer
    battery_size_map = {
        'AAA': 1,
        'AA': 2,
        'C': 3,
        'D': 4
    }
    df['Battery_Size'] = df['Battery_Size'].map(battery_size_map)

    #Map discharge speed to integer
    battery_size_map = {
        'Slow': 1,
        'Medium': 2,
        'Fast': 3
    }
    df['Discharge_Speed'] = df['Discharge_Speed'].map(battery_size_map)
    return df    


def calculate_statistic(
    measure: Literal["mean", "median", "mode"],
    column: pd.Series
) -> Union[float, pd.Series]:
    """
    Calculate the specified statistical measure for a given pandas DataFrame column.

    Args:
        measure (Literal["mean", "median", "mode"]): The statistical measure to calculate.
        column (pd.Series): The pandas DataFrame column to perform the calculation on.

    Returns:
        float: The calculated statistic.

    Raises:
        ValueError: If an invalid measure is provided.
    """
    if measure == "mean":
        return column.mean()
    elif measure == "median":
        return column.median()
    elif measure == "mode":
        column.mode()[0]
    
    else:
        raise ValueError("Invalid measure. Choose 'mean', 'median', or 'mode'.")




