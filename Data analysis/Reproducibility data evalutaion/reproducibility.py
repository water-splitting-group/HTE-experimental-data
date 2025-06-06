import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 14})  # Setze die Schriftgröße für alle Plots

# CSV-Datei einlesen
df = pd.read_csv(r'C:\Users\to86hug\Desktop\HTE experimental data\Data analysis\Reproducibility data evalutaion\2025-06-06T08-05_export.csv')

# Nehmen wir an, deine Spalte heißt 'messwerte'
messwerte = df['max rate ydiff']

# Berechnung des Mittelwerts
mean_value = messwerte.mean()

# Figure erstellen mit ansprechender Größe und Auflösung
plt.figure(figsize=(8, 6), dpi=100)

# OPTION 2: Boxplot (gut für statistische Verteilung)
# Datenpunkte hinzufügen (mit etwas Jitter für bessere Sichtbarkeit)
x = np.random.normal(1, 0.032, size=len(messwerte))
plt.scatter(x, messwerte,alpha=0.8, color='blue', s=80)
plt.boxplot(
    messwerte,
    boxprops=dict(linewidth=3),
    whiskerprops=dict(linewidth=3),
    capprops=dict(linewidth=3),
    medianprops=dict(linewidth=3),
    flierprops=dict(marker='o', markersize=0),  # hides white outliers
    whis=[0, 100]  # extend whiskers to min and max
)

# Mittelwert als roten Punkt hinzufügen
plt.scatter([1], [mean_value], color='darkgreen', marker= 'D', s=150)

plt.xlim(0.75, 1.25)
plt.ylabel('max. oxygen evolution rate / µM s$^{-2}$', fontsize=14)
plt.xlabel('Experiments for reproducibility tests', fontsize=14)
plt.xticks([])
plt.tight_layout()
plt.savefig('reproduzierbarkeitstest.png', dpi=300)  # Speichern in hoher Qualität
plt.show()