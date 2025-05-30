import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Read the data
data = pd.read_csv('AE-413-for_python.CSV', sep=';')

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
plt.scatter(data['pH'], data['ratio'], alpha=0.5, label='Experimental Data')
plt.plot(pH_smooth, ratio_smooth, 'r-', label='Power Law Fit')

plt.xlabel('pH')
plt.ylabel('Ratio')
plt.title('pH vs Ratio Relationship with Power Law Fit')
plt.legend()
plt.grid(True, alpha=0.3)

# Add fitted equation parameters
equation = f'ratio = {popt[0]:.2e} × pH^({popt[1]:.2f}) + {popt[2]:.2f}'
plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

# Calculate R-squared
residuals = data['ratio'] - power_law(data['pH'], *popt)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((data['ratio'] - np.mean(data['ratio'])) ** 2)
r_squared = 1 - (ss_res / ss_tot)

plt.text(0.05, 0.89, f'R² = {r_squared:.3f}', transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.8))

# Print the fitted parameters
print(f"Fitted parameters:")
print(f"a (scale factor): {popt[0]:.2e}")
print(f"b (power): {popt[1]:.2f}")
print(f"c (offset): {popt[2]:.2f}")
print(f"R-squared: {r_squared:.3f}")

plt.show()