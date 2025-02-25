###Kapitel 1: Data Laden




''' Richtiger Code '''

import pandas as pd
import numpy as np
from pathlib import Path


### Data Loading

DATA_FOLDER = Path("/Volumes/IAB-Daten-RV/leo/test/")  

""" ich musste hier mit pyreadstat arbeiten, weil der normale read.stata nBefehl nciht richtig ausgeführt wurde. 
Ich habe städngi die gleiche Fehlermeldung bekommen: Version of given Stata file is 0. pandas supports importing 
versions 105, 108, 111 (Stata 7SE), 113 (Stata 8/9), 114 (Stata 10/11), 115 (Stata 12), 117 (Stata 13), 
118 (Stata 14/15/16),and 119 (Stata 15/16, over 32,767 variables).


import pyreadstat

df, meta = pyreadstat.read_dta(str(DATA_FOLDER / "siab_copy_wo_w08_abgebj1930.dta"))  # Konkrete Datei auswählen

print(df.head())

"""

# Erstelle  Liste aller .dta-Dateien im Ordner. Diese Methode gibt dann meist die Fehlermeldung dass die stata-file nicht von der richtigen stata version 0 kommt. 
# Warum das so ist, habe ich noch nicht kapiert.
data_paths = list(DATA_FOLDER.glob("**/*.dta"))

def load_data(paths: list[Path]) -> pd.DataFrame:
    df_list = [pd.read_stata(path) for path in paths]  
    df = pd.concat(df_list, ignore_index=True)  
    return df

data = load_data(data_paths)
print(data.head())



# Kapitel 2: Datentypen umwandeln und column name changes


'''
# Spalten umbenennen, 1 zu1 von Marvin übernommen
def rename_columns(
    df: pd.DataFrame,
    rename_map: dict[str, str],
) -> pd.DataFrame:
    """Rename columns in DataFrame.

    Args:
    ----
    df : pd.DataFrame
        DataFrame with columns to rename.
    rename_map : dict
        Dictionary with old column names as keys and new column names as values.

    Returns:
    -------
    pd.DataFrame
        DataFrame with renamed columns.

    """
    return df.rename(columns=rename_map)
'''


'''
#'Datentypen umwandeln'
def change_d_types(
    df: pd.DataFrame,
    dtypes_map: dict[str, str],
) -> pd.DataFrame:
    """Change data types of columns in DataFrame.

    Args:
    ----
    df : pd.DataFrame
        DataFrame to change data types in.
    dtypes_map : dict
        Dictionary with column names as keys and new data types as values.

    Returns:
    -------
    pd.DataFrame
        DataFrame with changed data types.

    """
    return df.astype(dtypes_map, errors="raise")



### das ist hier eine angepasste version der dtypes funktion die die datenrtypen iwie besser umgeht. (???)


def change_d_types(
    df: pd.DataFrame,
    dtypes_map: dict[str, str],
) -> pd.DataFrame:
    """Change data types of columns in DataFrame."""
    # Stelle sicher, dass alle Datumswerte richtig konvertiert werden
    for col, dtype in dtypes_map.items():
        if dtype == 'datetime64[ns]':  # Überprüfen, ob der Zieltyp datetime ist
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            df[col] = df[col].astype(dtype, errors='raise')
    return df


change_d_types(df = df, dtypes_map=IAB_D_TYPES)

'''





#Kapitel 3: Neue Variabeln erstellen

'''
# Funktionen um neue Variablen zu erstellen 
### Erstellung der year Variabel



def generate_year_column(df, date_column):
    """
    Generates a 'year' column from a specified date column in the DataFrame.
    
    Parameters:
    - df: pandas DataFrame
    - date_column: Name of the column containing date information (string)
    
    Returns:
    - df: DataFrame with a new 'year' column
    """
    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    # Generate 'year' from the date column
    df['year'] = df[date_column].dt.year
    
    # Return the modified DataFrame
    return df


# Erstellung der Alter-Variablen. Ich muss mich hier natürlich ncoh auf die richtigen Varibalen festlegen. gebjahr und begorig als year_column (???)
import pandas as pd

# Funktion zur Berechnung des Alters
def calculate_age(df, year_column, birth_year_column):
    """
    Berechnet das Alter basierend auf den angegebenen Spalten für Jahr und Geburtsjahr.

    Args:
    - df (pd.DataFrame): Das DataFrame, das die Daten enthält.
    - year_column (str): Der Name der Spalte, die das Jahr (z.B. 'year') enthält.
    - birth_year_column (str): Der Name der Spalte, die das Geburtsjahr (z.B. 'birth_year') enthält.

    Returns:
    - pd.DataFrame: Das aktualisierte DataFrame mit der neuen Spalte 'age' und einem Label für das Alter.
    """
    # Berechne das Alter
    df['age'] = df[year_column] - df[birth_year_column]

    # Füge ein Label für das Alter hinzu (Englisch)
    df['age_label_en'] = 'age (in years)'

    return df

'''



'''
# Kapitel 3: splitten & ... 

# Splitten der Daten


def split_spells_in_one_function(df, persnr_col='persnr', spell_col='spell', start_col='begepi', end_col='endepi', gebjahr_col='gebjahr'):
    # Schritt 1: Sortieren der Daten nach den benutzerdefinierten Spalten
    df = df.sort_values(by=[persnr_col, spell_col])

    # Schritt 2: Berechnung der Anzahl der Jahre, die ein Spell abdeckt
    df['span_year'] = (df[end_col].dt.year - df[start_col].dt.year + 1)
    # Der berechnete Wert wird in einer neuen Spalte des DataFrames gespeichert, die den Namen span_year trägt.
    # Die Spalte span_year enthält nun für jede Zeile im DataFrame die Anzahl der Jahre, die der Spell abdeckt.

    # Schritt 3: Expandieren des DataFrames für jeden Jahrgang
    df_expanded = df.loc[df.index.repeat(df['span_year'])].reset_index(drop=True)
    # .reset_index() setzt den Index des DataFrames zurück, sodass er wieder von 0 aufwärts zählt. Das drop=True sorgt dafür, dass der alte Index nicht als neue Spalte gespeichert wird. 
    # Wenn du drop=False setzen würdest, würde der alte Index als zusätzliche Spalte in den DataFrame eingefügt werden. Beispiel: Wenn wir den oben beschriebenen Index [0, 0, 1, 1, 1] 
    # haben und .reset_index(drop=True) verwenden, dann wird der Index auf [0, 1, 2, 3, 4] zurückgesetzt.

    # Schritt 4: Start- und Enddaten für die neuen Zeilen anpassen
    df_expanded[end_col] = df_expanded.apply(
        lambda row: pd.Timestamp(year=row[start_col].year, month=12, day=31) if row.name == 0 else row[end_col], axis=1
    )

    df_expanded[start_col] = df_expanded.apply(
        lambda row: pd.Timestamp(year=row[start_col].year + 1, month=1, day=1) if row.name > 0 else row[start_col], axis=1
    )

    # Schritt 5: Berechnen des Jahres (jahr) und des Alters (age)
    df_expanded['jahr'] = df_expanded[start_col].dt.year
    df_expanded['age'] = df_expanded['jahr'] - df_expanded[gebjahr_col]

    # Schritt 6: Bereinigung (Entfernen der temporären Spalten)
    df_expanded = df_expanded.drop(columns=['span_year'])

    # Rückgabe des bearbeiteten DataFrames
    return df_expanded


# Anwendung der Funktion auf den DataFrame 'data'
df_split = split_spells_in_one_function(df=data, persnr_col='persnr', spell_col='spell', start_col='begepi', end_col='endepi', gebjahr_col='gebjahr')

# Ausgabe des bearbeiteten DataFrames
print(df_split.head)
'''

def split_spells_in_one_function(df, persnr_col='persnr_siab_r', spell_col='spell', start_col='begepi', end_col='endepi', gebjahr_col='gebjahr'):
    # Schritt 1: Sortieren der Daten nach den benutzerdefinierten Spalten
    df = df.sort_values(by=[persnr_col, spell_col])

    # Schritt 2: Berechnung der Anzahl der Jahre, die ein Spell abdeckt
    df['span_year'] = (df[end_col].dt.year - df[start_col].dt.year + 1)
    # Der berechnete Wert wird in einer neuen Spalte des DataFrames gespeichert, die den Namen span_year trägt.
    # Die Spalte span_year enthält nun für jede Zeile im DataFrame die Anzahl der Jahre, die der Spell abdeckt.

    # Schritt 3: Expandieren des DataFrames für jeden Jahrgang
    df_expanded = df.loc[df.index.repeat(df['span_year'])].reset_index(drop=True)
    # .reset_index() setzt den Index des DataFrames zurück, sodass er wieder von 0 aufwärts zählt. Das drop=True sorgt dafür, dass der alte Index nicht als neue Spalte gespeichert wird. 
    # Wenn du drop=False setzen würdest, würde der alte Index als zusätzliche Spalte in den DataFrame eingefügt werden. Beispiel: Wenn wir den oben beschriebenen Index [0, 0, 1, 1, 1] 
    # haben und .reset_index(drop=True) verwenden, dann wird der Index auf [0, 1, 2, 3, 4] zurückgesetzt.

    # Schritt 4: Start- und Enddaten für die neuen Zeilen anpassen
    df_expanded[end_col] = df_expanded.apply(
        lambda row: pd.Timestamp(year=row[start_col].year, month=12, day=31) if row.name == 0 else row[end_col], axis=1
    )

    df_expanded[start_col] = df_expanded.apply(
        lambda row: pd.Timestamp(year=row[start_col].year + 1, month=1, day=1) if row.name > 0 else row[start_col], axis=1
    )

    # Schritt 5: Berechnen des Jahres (jahr) und des Alters (age)
    df_expanded['jahr'] = df_expanded[start_col].dt.year
    df_expanded['age'] = df_expanded['jahr'] - df_expanded[gebjahr_col]

    # Schritt 6: Bereinigung (Entfernen der temporären Spalten)
    df_expanded = df_expanded.drop(columns=['span_year'])

    # Rückgabe des bearbeiteten DataFrames
    return df_expanded


# Anwendung der Funktion auf den DataFrame 'data'
df_split = split_spells_in_one_function(df=data, persnr_col='persnr', spell_col='spell', start_col='begepi', end_col='endepi', gebjahr_col='gebjahr')

# Ausgabe des bearbeiteten DataFrames
print(df_split.head)


# Kapitel 6: Deflation 

def generate_cpi(df, year_col='jahr'):
    """Mapped jedes Jahr im DataFrame auf seinen CPI-Wert aus cpi_values."""
    df['cpi'] = df[year_col].map(cpi_values)  # Direktes Mapping ohne Lambda
    return df



def calculate_real_wage(row):
    """Berechnet den deflationierten Lohn."""
    return 100 * row['tentgelt_gr'] / row['cpi'] if row['cpi'] else np.nan



