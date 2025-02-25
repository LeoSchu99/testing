# CLeaning RTZN data.


"""
📌 Wie funktioniert pytask genau?
Wenn du in einem Terminal oder einer Konsole einfach
pytask
eingibst, dann passiert Folgendes:
1️⃣ Pytask sucht nach task_*.py Dateien im aktuellen Projektordner
Es scannt die Python-Dateien, die mit task_ beginnen (z. B. task_clean_rtzn.py).
Diese Dateien enthalten @task-dekorierte Funktionen, also definierte Aufgaben.
2️⃣ Es analysiert alle Tasks, die es finden kann
Es schaut sich an, welche Abhängigkeiten (depends_on) und welche Ergebnisse (produces) es gibt.
Falls sich eine Abhängigkeit geändert hat (z. B. eine neue Stata-Datei wurde hinzugefügt), wird die zugehörige Task neu ausgeführt.
3️⃣ Nur die relevanten Tasks werden ausgeführt!
Falls sich keine Daten geändert haben, passiert nichts.
Falls eine Abhängigkeit aktualisiert wurde, wird die entsprechende Task neu berechnet.
"""

from pytask import task

from retirement_behavior.config import (
    BLD,
    RTZN_FOLDER,
)
from retirement_behavior.data_cleaning.clean import (
    clean_raw_data,
    compute_retirement_age,
    read_merged_rtzn_data,
    retirement_age_is_rounded,
)
from retirement_behavior.data_cleaning.cleaning_config import (
    CALENDAR_YEAR_UNTIL_AGES_ARE_ROUNDED,
    RTZN_COLUMN_RENAME_MAP,
    RTZN_D_TYPES,
    RTZN_DROP_IF_NA,
    RTZN_VALUE_REPLACE_MAP,
)

RTZN_DATA_PATHS = list(RTZN_FOLDER.glob("*/*.dta")) + list(RTZN_FOLDER.glob("*/*.DTA"))

""" Was passiert hier?
Es werden alle Stata-Dateien (.dta & .DTA) im RTZN_FOLDER gesucht.
Das Ergebnis ist eine Liste mit Datei-Pfaden, die später als Input für die Funktion dient.

1️⃣ Was macht RTZN_FOLDER.glob("*/*.dta")?
RTZN_FOLDER ist ein Pfad zu einem Ordner mit Daten.
.glob("*/*.dta") durchsucht alle Unterordner (*/*) nach Dateien mit der Endung .dta.
Es gibt eine Liste von Pfad-Objekten zurück, die zu diesen Dateien führen.

2️⃣ Warum gibt es zwei .glob()-Aufrufe?
list(RTZN_FOLDER.glob("*/*.dta")) + list(RTZN_FOLDER.glob("*/*.DTA"))
.dta und .DTA sind dasselbe Dateiformat (Stata-Dateien), aber Windows und andere Systeme machen manchmal einen Unterschied zwischen Groß- und Kleinschreibung.
Um sicherzustellen, dass ALLE Dateien gefunden werden, sucht der Code sowohl nach .dta als auch .DTA.
Die beiden Listen werden mit + zusammengefügt.

"""

@task
def task_clean_rtzn(
    depends_on=RTZN_DATA_PATHS,
    produces=BLD / "data" / "rtzn_cleaned.pickle",
):

"""
🔹 Was passiert hier?
@task → Dekorator von Pytask, um eine automatisierte Datenverarbeitung zu definieren.
depends_on=RTZN_DATA_PATHS → Die Funktion benötigt die Rohdaten als Eingabe.
produces=BLD / "data" / "rtzn_cleaned.pickle" → Das bereinigte Ergebnis wird als Pickle-Datei gespeichert.
👉 Kurz gesagt: Diese Funktion wird automatisch ausgeführt, wenn sich die Rohdaten ändern!
"""
    """Clean RTZN data.

    Do this using the following steps:
        1. Read in and concat RTZN waves.
        2. Rename columns.
        3. Replace values (e.g. strings with bools or ints).
        4. Change data types.
        5. Drop rows with NA values in specified columns.
        6. Filter out relevant columns.
        7. Compute retirement age.

    """
    rtzn_raw_data = read_merged_rtzn_data(depends_on).reset_index()

    """ 🔹 Was passiert hier?
Die Funktion read_merged_rtzn_data() lädt und kombiniert die RTZN-Daten aus mehreren Dateien.
.reset_index() sorgt dafür, dass der Index in eine normale Spalte umgewandelt wird.
"""


    rtzn_cleaned_data = clean_raw_data(
        rtzn_raw_data,
        rename_cols_map=RTZN_COLUMN_RENAME_MAP,
        replace_vals_map=RTZN_VALUE_REPLACE_MAP,
        nan_filter_columns=RTZN_DROP_IF_NA,
        dtypes_map=RTZN_D_TYPES,
    )
    """🔹 Was passiert hier?
clean_raw_data() führt mehrere Datenbereinigungs-Schritte aus:
✅ Spalten umbenennen (RTZN_COLUMN_RENAME_MAP)
✅ Werte ersetzen (RTZN_VALUE_REPLACE_MAP)
✅ Zeilen mit NaN entfernen (RTZN_DROP_IF_NA)
✅ Datentypen anpassen (RTZN_D_TYPES)
📌 Ergebnis: Das DataFrame ist sauber & einheitlich formatiert.
"""

"""
wann braucht man das out und wann nciht?
Die clean_raw_data()-Funktion nimmt ein DataFrame (rtzn_raw_data), führt alle Bereinigungsschritte durch 
und gibt es direkt zurück. Daher wird das Ergebnis direkt rtzn_cleaned_data zugewiesen, 
ohne eine zusätzliche Variable (out) zu verwenden.

out = rtzn_cleaned_data[RTZN_D_TYPES.keys()]
🧐 Hier wird out explizit definiert, weil wir aus dem bereinigten DataFrame nur bestimmte Spalten behalten möchten.

rtzn_cleaned_data enthält alle Spalten nach der Bereinigung
RTZN_D_TYPES.keys() enthält eine Liste der erlaubten Spalten
out speichert das gefilterte DataFrame, das nur die gewünschten Spalten enthält
"""
    out = rtzn_cleaned_data[RTZN_D_TYPES.keys()]
    """ 🔹 Was passiert hier?
Es werden nur die Spalten beibehalten, die in RTZN_D_TYPES.keys() definiert sind.
Dadurch wird sichergestellt, dass keine unnötigen Spalten enthalten sind.
"""

    out["retirement_age"] = compute_retirement_age(
        retirement_age_m=rtzn_cleaned_data["retirement_age_m"],
        retirement_age_y=rtzn_cleaned_data["retirement_age_y"],
    )
    """
    🔹 Was passiert hier?
Die Funktion compute_retirement_age() berechnet das Renteneintrittsalter basierend auf zwei Spalten:
retirement_age_m: Rentenalter in Monaten
retirement_age_y: Rentenalter in Jahren

    """

    out["retirement_age"] = out["retirement_age"].fillna(
        out["retirement_age_agg_before_2014"],
    )
    """ 🔹 Was passiert hier?
Falls retirement_age fehlende Werte (NaN) hat, wird stattdessen retirement_age_agg_before_2014 genutzt.
"""
    out["retirement_age_is_rounded"] = retirement_age_is_rounded(  
        calendar_year=out["year"],
        calendar_year_until_ages_are_rounded=CALENDAR_YEAR_UNTIL_AGES_ARE_ROUNDED,
    )
    out["geburtsjahr"] = out["year"] - out["alter"]
    """
    🔹 Was passiert hier?
Das Geburtsjahr wird berechnet als Jahr - Alter.
    """
    out.set_index("year").to_pickle(produces)

    """
    🔹 Was passiert hier?
out.set_index("year") → Setzt die Jahreszahl als Index.
.to_pickle(produces) → Speichert das DataFrame als Pickle-Datei.

    """