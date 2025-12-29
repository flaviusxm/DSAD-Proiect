import os
import pandas as pd

director_date_excel = r'd:\DSAD-Proiect\pre-cleaning-data'
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
    "Euro area", "European Union", "High income", "Post-demographic dividend"
}

def extrage_perechi_tara_an(cale_fisier):
    try:
        df = pd.read_excel(cale_fisier, skiprows=3)
    except Exception as e:
        print(f"Eroare citire : {e}")
        return set()
    
    perechi_valide = set()
    coloane_ani = [col for col in df.columns if str(col).isdigit()]

    for index, rand in df.iterrows():
        tara = rand['Country Name']
        if tara in date_regiuni_excluse: continue
        
        for an in coloane_ani:
            valoare = rand[an]
            if pd.notna(valoare) and str(valoare).strip() != '..':
                perechi_valide.add((tara, int(an))) 
    return perechi_valide

#intersectia
date_comune = None


for fisier in fisiere_variabila_x + fisiere_variabila_y:
    date_curente = extrage_perechi_tara_an(fisier)
    
    if date_comune is None:
        date_comune = date_curente
    else:
        date_comune = date_comune.intersection(date_curente)



#analiza dupa an
ani_disponibili = sorted(list(set([an for tara, an in date_comune])))
max_tari = 0
cel_mai_bun_an = None
lista_tari_finale = []

for an in ani_disponibili:
    tari_in_an = sorted([tara for tara, y in date_comune if y == an])
    contor = len(tari_in_an)
    
    if contor >= max_tari:
        max_tari = contor
        cel_mai_bun_an = an
        lista_tari_finale = tari_in_an

print(f"Cel mai bun an este {cel_mai_bun_an} cu {max_tari} tari ")
print("Lista tari ", lista_tari_finale)