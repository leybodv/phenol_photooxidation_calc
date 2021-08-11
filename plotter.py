# TODO: docs

import math
import matplotlib.pyplot as plt
from experiment import Experiment
from datapoint import DataPoint
from calibrationpoint import CalibrationPoint

class Plotter():

    def plotrawdata(self, experiments):
        """
        """
        print(f'Plotter().plotrawdata(experiments):') #LOG
        if len(experiments) == 1:
            fig, ax = plt.subplots()
            self.plotrawexperiment(ax, experiments[0])
        else:
            exps_copy = experiments.copy()
            cols = math.ceil(math.sqrt(len(experiments)))
            rows = math.ceil(len(experiments) / cols)
            fig, axs = plt.subplots(nrows=rows, ncols=cols)
            print(f'{axs = }') #LOG
            for row in range(rows):
                for col in range(cols):
                    if not bool(exps_copy):
                        break
                    self.plotrawexperiment(axs[row,col], exps_copy.pop(0))
        plt.show()

    def plotrawexperiment(self, ax, experiment):
        """
        """
        print(f'Plotter().plotrawexperiment(ax, experiment):') #LOG
        ax.set_title(experiment.sample_name)
        for data_point in experiment.data_points:
            ax.plot(data_point.wavelength, data_point.absorbance, label=data_point.time)
            print(f'{ax.get_children() = }') #LOG
            print(f'{ax.get_children()[-1].get_label() = }') #LOG
        ax.legend()
        return ax

    def plot_raw_calibration(self, points):
        """
        """
        print(f'Plotter().plot_raw_calibration(points):') #LOG
        fig, ax = plt.subplots()
        for point in points:
            ax.plot(point.wavelength, point.absorbance, label=point.concentration)
        ax.legend()
        plt.show(block=False)
