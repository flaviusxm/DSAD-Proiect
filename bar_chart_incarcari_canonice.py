import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


date = {
    'Variabile': [
        'Înscriere Secundar (X3)', 
        'Înscriere Terțiar (X2)', 
        'Cheltuieli Educație (X1)',
        'Speranța de Viață (Y3)', 
        'Cheltuieli Sanatate (Y1)', 
        'Mortalitate Infantilă (Y2)'
    ],
    'Incarcari': [0.980, 0.871, 0.283, 0.953, 0.566, -0.988],
    'Set': ['Educatie (X)', 'Educatie (X)', 'Educatie (X)', 
            'Sanatate (Y)', 'Sanatate (Y)', 'Sanatate (Y)']
}

tabel_date_bar_chart = pd.DataFrame(date)
print(tabel_date_bar_chart)
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")


colors = {"Educatie (X)": "#4c72b0", "Sanatate (Y)": "#c44e52"} 
ax = sns.barplot(x='Incarcari', y='Variabile', hue='Set', data=tabel_date_bar_chart,palette=colors, dodge=False)


plt.axvline(0, color='black', linewidth=1)
plt.title('Încărcările Canonice - Funcția 1', fontsize=14, fontweight='bold')
plt.xlabel('Coeficient de Corelație (Structura)', fontsize=12)
plt.ylabel('')
plt.xlim(-1.1, 1.1) 
plt.legend(title='Set de Variabile', loc='lower right')


for i in ax.containers:
    ax.bar_label(i, fmt='%.3f', padding=3)

plt.tight_layout()
plt.savefig('charts/Incarcarile_Canonice.png', dpi=300)
plt.show()