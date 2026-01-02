import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

dataframe_date_csv=pd.read_csv('csv-cleaned-data/date-finale.csv',index_col=0)
variabilele_X=[
    'Cheltuieli_Guvernamentale_Educatie_%_PIB',
    'Inscrieri_Invatamant_Tertiar_%_Populatie',
    'Inscrieri_Invatamant_Secundar_%_Populatie'
]
variabilele_Y=[
    'Cheltuieli_Curente_Pentru_Sanatate_%_PIB',
    'Rata_Mortalitatii_Infantile_/1000',
    'Speranta_Viata_Ani'
]
mat_corelatie=dataframe_date_csv[variabilele_X + variabilele_Y].corr()
sns.heatmap(mat_corelatie ,annot=True,cmap='coolwarm',center=0,fmt=".2f",linewidths=0.5)
plt.title("Matricea de Corelatie - Educatie si Sanatate")
plt.savefig("charts/HeatMap_Corelatii.png",dpi=300)
