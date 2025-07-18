import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Read the data
data = pd.read_csv('experimental_data\pH_value_buffer\AE-413-for_python.CSV', sep=';')

# Sort data by pH to ensure smooth plotting
data = data.sort_values('pH')
data_for_fitting = data[20:] #omit first 20 data points (very high ratios) to better describe low ratio regime

# Define power law function
def power_law(x, a, b, c):
    """
    f(x) = a * x^b + c
    a: scale factor
    b: power (exponent)
    c: vertical offset
    """
    return a * np.power(x, b) + c

# Fit the power law function
popt, pcov = curve_fit(power_law, data_for_fitting['pH'], data_for_fitting['ratio'], 
                      p0=[1e10, -15, 0],  # Initial parameter guesses
                      maxfev=10000)


# Generate smooth curve for plotting
pH_smooth = np.linspace(data['pH'].min(), data['pH'].max(), 500)
ratio_smooth = power_law(pH_smooth, *popt)

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(data['pH'], data['ratio'], label='Experimental Data', color='blue')
plt.plot(pH_smooth, ratio_smooth, 'r-', label='Power Law Fit', color='green')

plt.xlabel('pH-value')
plt.ylabel('Bicrabonate / carbonate ratio / -')
plt.legend()

# Calculate R-squared
residuals = data['ratio'] - power_law(data['pH'], *popt)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((data['ratio'] - np.mean(data['ratio'])) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# equation = f'ratio = {popt[0]:.2e} × pH^({popt[1]:.2f}) + {popt[2]:.2f}'
# plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, 
#          bbox=dict(facecolor='white', alpha=0.8))

plt.show()