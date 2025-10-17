import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

# ==========================
# Configuration
# ==========================
FILE1_PATH = '2025-10-08_094932_AE-579-300-irrad.txt'  # PyroScience file 1
FILE2_PATH = '2025-10-08_105149_AE-579-10-irrad.txt'   # PyroScience file 2
FILE3_PATH = 'results_MRG-059-ZO-1C.csv'               # CSV file with uM_1

# Set start times
START_TIME_FILE1 = 450 - 400
START_TIME_FILE2 = 485 - 400
START_TIME_FILE3 = 1737627201 - 400  # Start timestamp for File 3

# ==========================
# Helper functions
# ==========================
def read_pyroscience_file(filepath):
    """Read PyroScience txt file, skipping header lines starting with #"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                lines = f.readlines()
            data_start = next(i for i, line in enumerate(lines) if not line.startswith('#'))
            df = pd.read_csv(filepath, sep='\t', skiprows=data_start, encoding=encoding)

            # Fix potential mojibake (e.g., “�mol” → “µmol”)
            df.columns = df.columns.str.replace('�', 'µ').str.strip()
            print(f"✅ Successfully read {filepath} using {encoding} encoding")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"⚠️ Error reading {filepath} with {encoding}: {e}")
    raise ValueError(f"❌ Could not read {filepath} with any of the attempted encodings: {encodings}")

def read_csv_file(filepath):
    """Read the CSV file"""
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    return df

def find_col(df, keyword):
    """Find the first column containing a keyword (case-insensitive)"""
    cols = [c for c in df.columns if keyword.lower() in c.lower()]
    return cols[0] if cols else None

# ==========================
# Read data
# ==========================
print("Reading files...")
df1 = read_pyroscience_file(FILE1_PATH)
df2 = read_pyroscience_file(FILE2_PATH)
df3 = read_csv_file(FILE3_PATH)

# ==========================
# Automatically detect PyroScience columns
# ==========================
time_col1 = find_col(df1, 'dt') or find_col(df1, 'time')
oxygen_col1 = find_col(df1, 'Oxygen')
time_col2 = find_col(df2, 'dt') or find_col(df2, 'time')
oxygen_col2 = find_col(df2, 'Oxygen')

print("\nDetected PyroScience columns:")
print(f"File 1: time='{time_col1}', oxygen='{oxygen_col1}'")
print(f"File 2: time='{time_col2}', oxygen='{oxygen_col2}'")

# ==========================
# Filter & standardize data
# ==========================
# File 1
df1_filtered = df1[df1[time_col1] >= START_TIME_FILE1].copy()
df1_filtered['time_adj'] = df1_filtered[time_col1] - START_TIME_FILE1
df1_filtered.rename(columns={oxygen_col1: 'oxygen'}, inplace=True)

# File 2
df2_filtered = df2[df2[time_col2] >= START_TIME_FILE2].copy()
df2_filtered['time_adj'] = df2_filtered[time_col2] - START_TIME_FILE2
df2_filtered.rename(columns={oxygen_col2: 'oxygen'}, inplace=True)

# File 3 (CSV)
df3_filtered = df3[df3['timestamp'] >= START_TIME_FILE3].copy()
df3_filtered['time_adj'] = df3_filtered['timestamp'] - START_TIME_FILE3
oxygen_col3 = 'uM_1'  # your desired column from the CSV
df3_filtered.rename(columns={oxygen_col3: 'oxygen'}, inplace=True)

# ==========================
# Clean NaNs
# ==========================
print("\n--- Filtering NaN values ---")
for i, df in enumerate([df1_filtered, df2_filtered, df3_filtered], start=1):
    if 'oxygen' not in df.columns:
        print(f"⚠️ File {i} has no column named 'oxygen'. Columns: {df.columns.tolist()}")
df1_filtered.dropna(subset=['oxygen'], inplace=True)
df2_filtered.dropna(subset=['oxygen'], inplace=True)
df3_filtered.dropna(subset=['oxygen'], inplace=True)

# ==========================
# Plotting
# ==========================
# === Plotting with custom x-axis start ===
t_start_label = -400  # the number you want the x-axis to start at

# Create new columns for plotting so the original data stays unchanged
df1_filtered['time_plot'] = df1_filtered['time_adj'] + t_start_label
df2_filtered['time_plot'] = df2_filtered['time_adj'] + t_start_label
df3_filtered['time_plot'] = df3_filtered['time_adj'] + t_start_label

fig, ax = plt.subplots(figsize=(12, 6))

# Plot each dataset using the shifted time
ax.plot(df1_filtered['time_plot'], df1_filtered['oxygen'],
        label='300 µM', marker='o', markersize=4, linestyle='None')
ax.plot(df2_filtered['time_plot'], df2_filtered['oxygen'],
        label='addition of 10 µM', marker='s', markersize=4, linestyle='None')
ax.plot(df3_filtered['time_plot'], df3_filtered['oxygen'],
        label='reference 10 µM', marker='^', markersize=4, linestyle='None')

# Customize axes limits (adjust as needed)
ax.set_xlim(t_start_label, t_start_label + 1200)  # for example, 2000 s range
ax.set_ylim(-1, 82)  # oxygen concentration limits

# Labels, title, legend, grid
ax.set_xlabel('Time / s', fontsize=14)
ax.set_ylabel(r'$O_2$ / $\mu$mol $L^{-1}$', fontsize=14)
ax.legend(loc='best', fontsize=14)

plt.tight_layout()
plt.savefig('oxygen_overlay_plot.png', dpi=300, bbox_inches='tight')
print("\n✅ Plot saved as 'oxygen_overlay_plot.png'")
plt.show()


# ==========================
# Summary Statistics
# ==========================
print("\n--- Summary Statistics ---")
print(f"File 1: {len(df1_filtered)} pts | Time: {df1_filtered['time_adj'].min():.2f}–{df1_filtered['time_adj'].max():.2f} s")
print(f"File 2: {len(df2_filtered)} pts | Time: {df2_filtered['time_adj'].min():.2f}–{df2_filtered['time_adj'].max():.2f} s")
print(f"File 3: {len(df3_filtered)} pts | Time: {df3_filtered['time_adj'].min():.2f}–{df3_filtered['time_adj'].max():.2f} s")
