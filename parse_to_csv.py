import os
import pandas as pd

director_date_excel = os.path.join('.', 'pre-cleaning-data')
fisiere_variabila_x = [os.path.join(director_date_excel, 'indicatori educatie X', f) for f in ['cheltuieli_guvern_educatie.xls', 'inscrieri_invatamant_tertiar.xls', 'inscrieri_invatamant_secundar.xls']]
fisiere_variabila_y = [os.path.join(director_date_excel, 'indicatori sanatate Y', f) for f in ['cheltuieli_curente_pentru_sanatate.xls', 'rata_mortalitatii_infantile.xls', 'speranta_de_viata_la_nastere.xls']]

date_regiuni_excluse = {
    "Africa Eastern and Southern", "Africa Western and Central", "Arab World", 
    "Central Europe and the Baltics", "Early-demographic dividend", "East Asia & Pacific", 
    "East Asia & Pacific (IDA & IBRD countries)", "East Asia & Pacific (excluding high income)", 
    "Europe & Central Asia", "Europe & Central Asia (IDA & IBRD countries)", 
    "Europe & Central Asia (excluding high income)", "Fragile and conflict affected situations", 
    "Heavily indebted poor countries (HIPC)", "IBRD only", "IDA & IBRD total", 
    "IDA blend", "IDA only", "IDA total", "Late-demographic dividend", 
    "Latin America & Caribbean", "Latin America & Caribbean (excluding high income)", 
    "Latin America & the Caribbean (IDA & IBRD countries)", "Least developed countries: UN classification", 
    "Low & middle income", "Low income", "Lower middle income", 
    "Middle East, North Africa, Afghanistan & Pakistan", "Middle income", 
    "North America", "Other small states", "OECD members", "Pre-demographic dividend", 
    "Small states", "South Asia", "South Asia (IDA & IBRD)", 
    "Sub-Saharan Africa", "Sub-Saharan Africa (IDA & IBRD countries)", 
    "Sub-Saharan Africa (excluding high income)", "Upper middle income", "World", 
    "Euro area", "European Union", "High income", "Post-demographic dividend","Caribbean small states"
}
an_pentru_analiza = "2015"

nume_coloane_noi = {
    'cheltuieli_guvern_educatie.xls': 'Cheltuieli_Guvernamentale_Educatie_%_PIB',
    'inscrieri_invatamant_tertiar.xls': 'Inscrieri_Invatamant_Tertiar_%_Populatie',
    'inscrieri_invatamant_secundar.xls': 'Inscrieri_Invatamant_Secundar_%_Populatie',
    'cheltuieli_curente_pentru_sanatate.xls': 'Cheltuieli_Curente_Pentru_Sanatate_%_PIB',
    'rata_mortalitatii_infantile.xls': 'Rata_Mortalitatii_Infantile_/1000',
    'speranta_de_viata_la_nastere.xls': 'Speranta_Viata_Ani' 
}

def extrage(lista_fisiere, an):
    df_acumulat = None
    
    for cale in lista_fisiere:

        df = pd.read_excel(cale, skiprows=3)
        nume_fisier = os.path.basename(cale)
        
        
        df = df[~df['Country Name'].isin(date_regiuni_excluse)]
        
        df_redus = df[['Country Name', an]].copy()
  
        df_redus[an] = pd.to_numeric(df_redus[an], errors='coerce')
        
        
        nume_nou = nume_coloane_noi.get(nume_fisier, nume_fisier)
        df_redus = df_redus.rename(columns={an: nume_nou})
        if df_acumulat is None:
            df_acumulat = df_redus
        else:
            df_acumulat = pd.merge(df_acumulat, df_redus, on='Country Name', how='inner')
            
    return df_acumulat

df_variabila_x = extrage(fisiere_variabila_x, an_pentru_analiza)
df_variabila_y = extrage(fisiere_variabila_y, an_pentru_analiza)

df_final = pd.merge(df_variabila_x, df_variabila_y, on='Country Name', sort=True, how='inner').dropna()

coloane_pentru_rotunjit = df_final.columns.difference(['Country Name'])
df_final[coloane_pentru_rotunjit] = df_final[coloane_pentru_rotunjit].round(2)

cale_salvare = os.path.join('.', 'csv-cleaned-data', 'date_finale.csv')
df_final.to_csv(cale_salvare, index=False)


print(f"Datele au fost salvate")
