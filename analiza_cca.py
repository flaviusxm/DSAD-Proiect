import numpy as np
import pandas as pd
import scipy.stats as stts
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

def nan_replace(t):
    nume_variabile = list(t.columns)
    for each in nume_variabile:
        if any(t[each].isna()):
            if is_numeric_dtype(t[each]):
                t[each].fillna(t[each].mean(), inplace=True)
            else:
                t[each].fillna(t[each].mode()[0], inplace=True)

def test_bartlett(r2, n, p, q, m):
    v = 1 - r2
    chi2 = (-n + 1 + (p + q + 1) / 2) * np.log(np.flip(np.cumprod(np.flip(v))))
    nlib = [(p - k + 1) * (q - k + 1) for k in range(1, m + 1)]
    p_values = 1 - stts.chi2.cdataframe_date_csv(chi2, nlib)
    return p_values


dataframe_date_csv = pd.read_csv('csv-cleaned-data/date_finale.csv', index_col=0)
nan_replace(dataframe_date_csv)


variabilele_X = ['Cheltuieli_Guvernamentale_Educatie_%_PIB',
           'Inscrieri_Invatamant_Tertiar_%_Populatie',
           'Inscrieri_Invatamant_Secundar_%_Populatie']

variabilele_Y = ['Cheltuieli_Curente_Pentru_Sanatate_%_PIB',
           'Rata_Mortalitatii_Infantile_/1000',
           'Speranta_Viata_Ani']


scaler = StandardScaler()
X_sc = scaler.fit_transform(dataframe_date_csv[variabilele_X])
Y_sc = scaler.fit_transform(dataframe_date_csv[variabilele_Y])


m = min(len(variabilele_X), len(variabilele_Y))
cca = CCA(n_components=m)
X_c, Y_c = cca.fit_transform(X_sc, Y_sc)


r = np.array([np.corrcoef(X_c[:, i], Y_c[:, i])[0, 1] for i in range(m)])
r2 = r**2


n = len(dataframe_date_csv)
p = len(variabilele_X)
q = len(variabilele_Y)
p_values = test_bartlett(r2, n, p, q, m)

print("Corelatii canonice (R):", r)
print("P-values (Bartlett):", p_values)


loadings_X = np.corrcoef(X_sc.T, X_c.T)[:p, p:]
loadings_Y = np.corrcoef(Y_sc.T, Y_c.T)[:q, q:]

t_loadings_X = pd.DataFrame(loadings_X, index=variabilele_X, columns=[f"U{i+1}" for i in range(m)])
t_loadings_Y = pd.DataFrame(loadings_Y, index=variabilele_Y, columns=[f"V{i+1}" for i in range(m)])

print("\n--- Loadings Set X ---\n", t_loadings_X)
print("\n--- Loadings Set Y ---\n", t_loadings_Y)

plt.figure(figsize=(10, 7))
plt.scatter(X_c[:, 0], Y_c[:, 0], color='skyblue', edgecolors='k', alpha=0.8)
plt.title(f"Scoruri Canonice: Educatie vs Sanatate\n(R={r[0]:.4f}, p={p_values[0]:.4e})")
plt.xlabel("Variabila Canonica Educatie (U1)")
plt.ylabel("Variabila Canonica Sanatate (V1)")
plt.axhline(0, color='grey', lw=1)
plt.axvline(0, color='grey', lw=1)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

weights_X = cca.x_weights_
weights_Y = cca.y_weights_

print("\n--- Coeficienți pentru Ecuația U1   ---")
for i, name in enumerate(variabilele_X):
    print(f"{name}: {weights_X[i, 0]:.4f}")

print("\n--- Coeficienți pentru Ecuația V1 ---")
for i, name in enumerate(variabilele_Y):
    print(f"{name}: {weights_Y[i, 0]:.4f}")


cross_loadings_X = np.corrcoef(X_sc.T, Y_c.T)[:p, p:]
cross_loadings_Y = np.corrcoef(Y_sc.T, X_c.T)[:q, q:]

t_cross_X = pd.DataFrame(cross_loadings_X, index=variabilele_X, columns=[f"V{i+1}" for i in range(m)])
t_cross_Y = pd.DataFrame(cross_loadings_Y, index=variabilele_Y, columns=[f"U{i+1}" for i in range(m)])

print("\n--- Cross-Loadings (X vs V) ---\n", t_cross_X)
print("\n--- Cross-Loadings (Y vs U) ---\n", t_cross_Y)


def analiza_redundanta(loadings, r2):
    shared_variance = np.mean(loadings**2, axis=0)
    redundancy = shared_variance * r2
    return shared_variance, redundancy

shared_X, redund_X = analiza_redundanta(loadings_X, r2)
shared_Y, redund_Y = analiza_redundanta(loadings_Y, r2)

print(f"\nVarianța extrasă din X de către U1: {shared_X[0]*100:.2f}%")
print(f"Redundanța (X explicat de V1): {redund_X[0]*100:.2f}%")
print(f"Varianța extrasă din Y de către V1: {shared_Y[0]*100:.2f}%")
print(f"Redundanța (Y explicat de U1): {redund_Y[0]*100:.2f}%")


