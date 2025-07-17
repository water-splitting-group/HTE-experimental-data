import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
from pathlib import Path
#import find_nearest as fn

def import_txt(file_path, channel, sensors):
	file = Path(file_path)


	raw_data = np.genfromtxt(file, skip_header=14+(2*sensors-2), encoding='ISO8859', usecols = (0,1,2,3,4,5,6,7,8,9,10,11))
	data = raw_data[:,[2, 2+channel, 6+channel]]
	return data


class Experiment:
	def __init__(self, file_path, channel = 1, sensors = 1):
		self.name = Path(file_path).stem  # Extracts filename without extension
		self.data = import_txt(file_path, channel, sensors)


	def plot_data(self, ax = plt, legend = True):

		ax.plot(self.data[:,0], self.data[:,1], label = "Septum pierced approx. 20 times", color = 'blue', linewidth = 1.5)
		ax.set_xlim(0, 1350)
		ax.set_ylim(-2.5, 18.5)
		
		# Add the first red horizontal line at e.g. time = 600 s
		first_line_time = 20  # adjust if needed
		ax.axvline(x=first_line_time, color='red', linestyle='--', linewidth=1)

		# Add second red line 20 minutes (1200 s) after the first
		second_line_time = first_line_time + 1200
		ax.axvline(x=second_line_time, color='red', linestyle='--', linewidth=1)

		if legend is True:
			ax.legend()

		if ax is not plt:
			ax.set_xlabel('Time / s')
			ax.set_ylabel(r'$O_2$ / $\mu$mol $l^{-1}$')


	def plot_temperature(self):

		plt.plot(self.data[:,0], self.data[:,2], label = self.name)
		plt.legend()

def main():

	exp = Experiment(
    r"C:\Users\to86hug\Desktop\HTE experimental data\Experimental Data\Leakage test\septum punctured 40 times\2024-04-03_091640_AE-250-2-Ch1.txt",
    channel = 1,
    sensors = 1
)


	fig, ax = plt.subplots()

	exp.plot_data(ax = ax, legend = True)

	return fig

if __name__ == '__main__':
	main()
	plt.show()