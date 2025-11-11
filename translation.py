# Assuming your DataFrame is currently named 'df'
import pandas as pd

df = pd.read_csv('Tango_Dataset_2025.csv',index_col='Unnamed: 0')

# Define the mapping dictionary: {'Old Name': 'new_name'}
column_renaming_map = {
    'Título': 'Title',
    'Género': 'Genre',
    'Subgénero': 'Subgenre',
    'Enlace': 'Link',
    'Tiene Letra': 'Has_Lyrics',
    'Tiene Partitura': 'Has_Sheet_Music',
    'Tiene Video': 'Has_Video',
    'Tiene Audio': 'Has_Audio',
    'Género_idx': 'Genre_ID',
    'Downloaded': 'Is_Downloaded'  # Using 'Is_Downloaded' for clarity
}

# Apply the rename operation
# We use 'errors="ignore"' to skip renaming any columns that don't exist
df.rename(columns=column_renaming_map, inplace=True)

print("✅ Columnas renombradas y estandarizadas.")
print(df.columns.tolist())

df.to_csv('Tango_Dataset_2025_EN.csv')