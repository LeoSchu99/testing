# Marvins SupaDupa Code

'''

def clean_raw_data(
    df: pd.DataFrame,
    rename_cols_map: dict[str, str],
    replace_vals_map: dict[str, str],
    nan_filter_columns: list[str],
    dtypes_map: dict[str, str],
) -> pd.DataFrame:
    


"""
Hier wird die Funktion clean_raw_data definiert.
In der Klammer stehen die Argumente, die die Funktion benötigt
"""

    """Clean raw data.

    Args:
    ----
    df : pd.DataFrame
        Raw data to clean.
    rename_cols_map : dict
        Dictionary with old column names as keys and new column names as values.
    replace_vals_map : dict
        Dictionary with old values as keys and new values as values.
    nan_filter_columns : list
        Columns to filter for nan values.
    dtypes_map : dict
        Dictionary with column names as keys and new data types as values.

    Returns:
    -------
    pd.DataFrame
        Cleaned data.

    """
    out = copy.deepcopy(df)
    """Das ursprüngliche df wird tief kopiert (deepcopy bedeutet: wirklich alle Daten werden kopiert, nicht nur die Referenz).
Dadurch bleibt das Original-df unverändert, falls man später darauf zurückgreifen will."""
    out = rename_columns(rename_map=rename_cols_map, df=out)
    out = replace_values_in_df(
        replace_map=replace_vals_map,
        df=out, )
    out = drop_rows_with_na(
        nan_filter_columns=nan_filter_columns,
        df=out,
    )
    return change_d_types( """hier wird das df aus dem letzten schritt genommen und in die change_d_types Funk
    tion gegeben und wir schreiben hier nciht mehr out sondern return,  weil das der letzte Schritt ist und 
    wir danach mit diesem Ergebnis dieser Funktion weiterarbeiten können"""
        dtypes_map=dtypes_map,
        df=out,
    )




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