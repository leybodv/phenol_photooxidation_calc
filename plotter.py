# TODO: docs

import math
import matplotlib.pyplot as plt
from experiment import Experiment
from datapoint import DataPoint
from calibrationpoint import CalibrationPoint
from result import Result
from resultpoint import ResultPoint

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
        plt.show(block=False)

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

    def plot_calibration(self, calibration):
        """
        """
        print(f'Plotter().plot_calibration(self, calibration):') #LOG
        fig, (ax_uvvis, ax_calibration) = plt.subplots(ncols=2)
        calibration_x = list()
        calibration_y_data = list()
        calibration_y_calc = list()
        for point in calibration.calibration_points:
            ax_uvvis.plot(point.wavelength, point.absorbance, label=point.concentration)
            calibration_x.append(point.concentration)
            calibration_y_data.append(point.get_absorbance_at(calibration.calibration_wavelength))
            calibration_y_calc.append(calibration.linear_func(point.concentration, calibration.calibration_coefficient))
        ax_uvvis.axvline(x=calibration.calibration_wavelength, color='red')
        ax_calibration.scatter(calibration_x, calibration_y_data, c='red')
        ax_calibration.plot(calibration_x, calibration_y_calc, c='blue')
        ax_uvvis.legend()
        plt.show(block=False)

    def plot_results(self, results:list):
        """
        """
        print(f'Plotter().plot_results(self, results):') #LOG
        if len(results) == 1:
            fig, ax = plt.subplots()
            self.plotresult(ax, results[0])
        else:
            rests_copy = results.copy()
            cols = math.ceil(math.sqrt(len(results)))
            rows = math.ceil(len(results) / cols)
            fig, axs = plt.subplots(nrows=rows, ncols=cols)
            for row in range(rows):
                for col in range(cols):
                    if not bool(rests_copy):
                        break
                    self.plotresults(axs[row,col], rests_copy.pop(0))
        plt.show(block=False)

    def plotresult(self, ax:Axes, result:Result) -> Axes:
        """
        """
        print(f'Plotter().plotresult(self, ax, result)') #LOG
        ax.set_title(result.get_name())
        points_dict = {}
        for point in result.get_points():
            for name, concentration in zip(point.get_reference_names(), point.get_concentrations()):
                if name not in points_dict:
                    points_dict[name] = (list(), list())
            points_dict[name][0].append(point.get_time())
            points_dict[name][1].append(concentration)
        for name in points_dict:
            ax.plot(points_dict[name][0], points_dict[name][1], label=name)
        ax.legend()
        return ax
