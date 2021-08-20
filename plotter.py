# TODO: docs

import math
import matplotlib.pyplot as plt
import numpy as np
from datapoint import DataPoint
from result import Result
from resultpoint import ResultPoint

class Plotter():

    def plotrawdata(self, experiments):
        """
        """
        if len(experiments) == 1:
            fig, ax = plt.subplots()
            self.plotrawexperiment(ax, experiments[0])
        else:
            exps_copy = experiments.copy()
            cols = math.ceil(math.sqrt(len(experiments)))
            rows = math.ceil(len(experiments) / cols)
            fig, axs = plt.subplots(nrows=rows, ncols=cols)
            for row in range(rows):
                for col in range(cols):
                    if not bool(exps_copy):
                        break
                    self.plotrawexperiment(axs[row,col], exps_copy.pop(0))
        plt.show(block=False)

    def plotrawexperiment(self, ax, experiment):
        """
        """
        ax.set_title(experiment.sample_name)
        for data_point in experiment.data_points:
            ax.plot(data_point.get_wavelength(), data_point.get_absorbance(), label=data_point.time)
        ax.legend()
        return ax

    def plot_raw_calibration(self, points, compound):
        """
        """
        fig, ax = plt.subplots()
        ax.set_title(compound)
        for point in points:
            ax.plot(point.get_wavelength(), point.get_absorbance(), label=point.get_concentration())
        ax.legend()
        plt.show(block=False)

    def plot_calibration(self, calibration):
        """
        """
        fig, (ax_uvvis, ax_calibration) = plt.subplots(ncols=2)
        calibration_x = list()
        calibration_y_data = list()
        calibration_y_calc = list()
        for point in calibration.calibration_points:
            ax_uvvis.plot(point.get_wavelength(), point.get_absorbance(), label=point.get_concentration())
            calibration_x.append(point.get_concentration())
            calibration_y_data.append(point.get_absorbance_at(calibration.calibration_wavelength))
            calibration_y_calc.append(calibration.linear_func(point.get_concentration(), calibration.calibration_coefficient))
        ax_uvvis.axvline(x=calibration.calibration_wavelength, color='red')
        ax_calibration.scatter(calibration_x, calibration_y_data, c='red')
        ax_calibration.plot(calibration_x, calibration_y_calc, c='blue')
        ax_uvvis.legend()
        plt.show(block=False)

    def plot_results(self, results:list):
        """
        """
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
                    self.plotresult(axs[row,col], rests_copy.pop(0))
        plt.show(block=False)

    def plotresult(self, ax:plt.Axes, result:Result) -> plt.Axes:
        """
        """
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

    def plot_result_point(self, datapoint:DataPoint, resultpoint:ResultPoint):
        """
        """
        fig, ax = plt.subplots()
        ax.plot(datapoint.get_wavelength(), datapoint.get_absorbance(), label='raw data')
        sum_absorbance = np.full(len(datapoint.get_absorbance()), 0)
        for reference_name, corrected_reference_spectrum in zip(resultpoint.get_reference_names(), resultpoint.get_corrected_reference_spectra()):
            ax.plot(corrected_reference_spectrum.get_wavelength(), corrected_reference_spectrum.get_absorbance(), linestyle='--', label=reference_name)
            sum_absorbance = sum_absorbance + corrected_reference_spectrum.get_absorbance()
        ax.plot(datapoint.get_wavelength(), sum_absorbance, label='sum')
        ax.legend()
        plt.show(block=False)
