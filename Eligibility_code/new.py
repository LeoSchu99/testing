Main Code - Notizen



import pandas as pd
import numpy as np
from pathlib import Path

Vorschlag zum generellen Vorgehen von GPT: 

# Schritt 1: Daten laden
def load_data(paths: list[Path]) -> pd.DataFrame:
    """Liest alle Daten und kombiniert sie in einem einzigen DataFrame."""
    df_list = [pd.read_stata(path) for path in paths]
    return pd.concat(df_list, ignore_index=True)

# Schritt 2: Spalten umbenennen
def rename_columns(df: pd.DataFrame, rename_map: dict[str, str]) -> pd.DataFrame:
    """Benennt Spalten basierend auf einem Mapping um."""
    return df.rename(columns=rename_map)

# Schritt 3: Fehlende Werte behandeln
def handle_missing_values(df: pd.DataFrame, nan_columns: list[str]) -> pd.DataFrame:
    """Ersetzt NaN-Werte durch sinnvolle Defaults."""
    for col in nan_columns:
        df[col] = df[col].fillna(0)  # Beispiel: Ersetze NaN mit 0
    return df

# Schritt 4: Einkommen inflationsbereinigt berechnen
def adjust_income_for_inflation(df: pd.DataFrame, income_col: str, inflation_rate: float) -> pd.DataFrame:
    """Passt Einkommen an die Inflation an."""
    df[income_col] = df[income_col] / (1 + inflation_rate)
    return df

# Schritt 5: Aggregation über den Lebenszyklus
def aggregate_lifecycle_variables(df: pd.DataFrame, groupby_col: str, agg_rules: dict) -> pd.DataFrame:
    """Aggregiert Variablen über den Lebenszyklus."""
    return df.groupby(groupby_col).agg(agg_rules).reset_index()

# Schritt 6: Die gesamte Cleaning-Pipeline definieren
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Wendet alle Cleaning-Schritte nacheinander an."""
    df = rename_columns(df, rename_map={"alte_spalte": "neue_spalte"})
    df = handle_missing_values(df, nan_columns=["arbeitsjahre", "einkommen"])
    df = adjust_income_for_inflation(df, income_col="einkommen", inflation_rate=0.02)
    df = aggregate_lifecycle_variables(df, groupby_col="id", agg_rules={"einkommen": "mean", "arbeitsjahre": "sum"})
    return df

# Schritt 7: Daten speichern
def save_cleaned_data(df: pd.DataFrame, path: Path):
    """Speichert das bereinigte DataFrame."""
    df.to_pickle(path)

# Hauptfunktion: Führt alle Schritte aus
def main():
    paths = list(Path("data/").glob("*.dta"))  # Alle Stata-Dateien laden
    raw_data = load_data(paths)
    cleaned_data = clean_data(raw_data)
    save_cleaned_data(cleaned_data, Path("data/cleaned_data.pickle"))

if __name__ == "__main__":
    main()











# Angenommen, wir haben bereits einen DataFrame `df` geladen, der die Spalten 'begepi' (Beispiel: Geburtsdatum) und 'gebjahr' enthält.
# Hier wird davon ausgegangen, dass die 'begepi'-Spalte ein Datetime-Objekt ist.

# 1. Erzeuge die Variable 'jahr' (Jahr)
df['jahr'] = df['begepi'].dt.year  # Extrahiert das Jahr aus dem 'begepi'-Datumsfeld

# 2. Erzeuge die Variable 'age' (Alter)
df['age'] = df['jahr'] - df['gebjahr']

# Beschriftung der Variablen (dies ist in Python nicht direkt verfügbar wie in Stata, aber man kann die Spaltenbezeichner mit einem Dictionary verknüpfen)
variable_labels = {
    'jahr': {'de': 'Jahr', 'en': 'year'},
    'age': {'de': 'Alter (in Jahren)', 'en': 'age (in years)'}
}

# Ausgabe der ersten Zeilen des DataFrames zur Überprüfung
print(df.head())
