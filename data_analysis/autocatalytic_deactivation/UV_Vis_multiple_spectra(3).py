import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

def parse_uvvis_file(filepath):
    """
    Parse UV/Vis spectrum file and extract wavelength and absorbance data.
    
    Args:
        filepath (str): Path to the spectrum file
        
    Returns:
        tuple: (wavelength_array, absorbance_array, filename_for_legend)
    """
    try:
        # Read the file, skipping header lines until we reach the data
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        
        # Find where the data starts (look for the header with "Wave" and "Absorbance")
        data_start_idx = 0
        for i, line in enumerate(lines):
            if 'Wave' in line and 'Absorbance' in line:
                data_start_idx = i + 1
                break
        
        # Extract data
        wavelengths = []
        absorbances = []
        
        for line in lines[data_start_idx:]:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                try:
                    # Split by semicolon and extract wavelength and absorbance
                    parts = line.split(';')
                    if len(parts) >= 5:  # Ensure we have enough columns
                        wavelength = float(parts[0].replace(',', '.'))  # Handle European decimal notation
                        absorbance = float(parts[4].replace(',', '.'))  # Absorbance is in column 5
                        wavelengths.append(wavelength)
                        absorbances.append(absorbance)
                except (ValueError, IndexError):
                    continue  # Skip problematic lines
        
        # Get filename for legend (without extension)
        filename = os.path.splitext(os.path.basename(filepath))[0]
        
        return np.array(wavelengths), np.array(absorbances), filename
    
    except Exception as e:
        print(f"Error reading file {filepath}: {str(e)}")
        return None, None, None

def plot_uvvis_spectra(file_list, folder_path=".", title="UV/Vis Spectra", 
                      xlim=None, ylim=None, save_plot=False, output_name="uvvis_spectra.png", legend_names=None):
    """
    Plot multiple UV/Vis spectra on the same graph.
    
    Args:
        file_list (list): List of filenames to plot
        folder_path (str): Path to folder containing the files
        title (str): Title for the plot
        xlim (tuple): X-axis limits as (min, max)
        ylim (tuple): Y-axis limits as (min, max)
        save_plot (bool): Whether to save the plot
        output_name (str): Filename for saved plot
        legend_names (list): Optional list of legend names corresponding to files
    """
    plt.figure(figsize=(10, 6))
    
    # Define your own color list
    custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    colors = [custom_colors[i % len(custom_colors)] for i in range(len(file_list))]
    
    plotted_count = 0
    
    for i, filename in enumerate(file_list):
        filepath = os.path.join(folder_path, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File '{filepath}' not found. Skipping...")
            continue
            
        wavelengths, absorbances, legend_name = parse_uvvis_file(filepath)
        
        if wavelengths is not None and absorbances is not None:
            # ✅ Use custom legend if provided
            label = legend_names[i] if legend_names and i < len(legend_names) else legend_name
            
            plt.plot(wavelengths, absorbances, 
                     color=colors[i], 
                     label=label, 
                     linewidth=1.5)
            plotted_count += 1
        else:
            print(f"Warning: Could not parse data from '{filename}'. Skipping...")
    
    if plotted_count == 0:
        print("Error: No spectra could be plotted. Check your file list and paths.")
        return
    
    # Customize the plot
    plt.xlabel('Wavelength / nm')
    plt.ylabel('Absorbance / -')
    plt.legend(loc='upper right')
    
    # Set axis limits if provided
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    
    plt.tight_layout()
    
    # Save plot if requested
    if save_plot:
        plt.savefig(output_name, dpi=300, bbox_inches='tight')
        print(f"Plot saved as '{output_name}'")
    
    plt.show()
    
    print(f"Successfully plotted {plotted_count} spectra.")

# Example usage
if __name__ == "__main__":
    # Specify the files you want to plot
    files_to_plot = [
        "AE-579-300-1_7420287SP.txt",
        "AE-579-300-2_7420287SP.txt",
        "AE-579-10-1_7420287SP.txt",
        "AE-579-10-2_7420287SP.txt" # Your example file
        # Add more filenames here as needed
        # "spectrum2.txt",
        # "spectrum3.txt",
    ]
    
    # Specify the folder containing your spectrum files
    folder_path = "."  # Current directory, change as needed
    
    # Plot the spectra
    plot_uvvis_spectra(
        file_list=files_to_plot,
        folder_path=folder_path,
        xlim=(300, 800),  # Wavelength range in nm
        ylim=(-0.01, 1.5),  # Auto-scale Y axis, or set like (0, 2) for specific range
        save_plot=True,  # Set to True if you want to save the plot
        output_name="AE-579.png",
        legend_names=["300 µM before irradiation", "300 µM after irradiation", "10 µM before irradiation", "10 µM after irradiation"]
    )