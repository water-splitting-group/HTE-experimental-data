import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
from pathlib import Path
import find_nearest as fn

def import_txt(name, channel, sensors):

	p = Path(r'C:\Users\to86hug\Downloads\AE-250-2-Ch1')
	file = p / name

	raw_data = np.genfromtxt(file, skip_header=14+(2*sensors-2), encoding='ISO8859', usecols = (0,1,2,3,4,5,6,7,8,9,10,11))
	data = raw_data[:,[2, 2+channel, 6+channel]]
	return data


class Experiment:

	def __init__(self, name, channel = 1, sensors = 1):
		self.name = name
		self.data = import_txt(self.name, channel, sensors)

	def plot_data(self, ax = plt, legend = True):

		ax.plot(self.data[:,0], self.data[:,1], label = "Septum pierced approx. 20 times", color = 'blue', linewidth = 1.5)
		ax.set_xlim(0, 1350)
		ax.set_ylim(-2.5, 18.5)
		
		if legend is True:
			ax.legend()

		if ax is not plt:
			ax.set_xlabel('Time / s')
			ax.set_ylabel(r'$O_2$ / $\mu$mol $l^{-1}$')
	#		ax.grid(color = 'grey', linestyle = '--', linewidth = 0.2)

	def plot_temperature(self):

		plt.plot(self.data[:,0], self.data[:,2], label = self.name)
		plt.legend()

def main():

	exp = Experiment('AE-251-2-Ch1.txt', channel = 1, sensors = 1)
	#'190125_JS_526_2.txt'

	fig, ax = plt.subplots()

	exp.plot_data(ax = ax, legend = True)

	return fig

if __name__ == '__main__':
	main()
	plt.show()