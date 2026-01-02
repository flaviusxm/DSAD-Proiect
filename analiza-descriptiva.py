import pandas as pd
tabel_data_frame = pd.read_csv('csv-cleaned-data/date_finale.csv')
statistici = tabel_data_frame.describe().transpose()
tabel_st_descriptive = statistici[['mean', 'std', 'min', 'max']]
print(tabel_st_descriptive.round(2))