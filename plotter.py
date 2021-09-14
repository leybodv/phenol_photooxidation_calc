import math
import matplotlib.pyplot as plt
import numpy as np
from datapoint import DataPoint
from result import Result
from resultpoint import ResultPoint
from experiment import Experiment

class Plotter():
    """
    utility class for plotting different types of data
    """

    def plotrawexperiment(self, ax, experiment):
        """
        plots single experimental data, i.e. uv-vis spectra at different times of experiment

        parameters
        ----------
        ax : matplotlib.Axes
            axes to plot to
        experiment : Experiment
            experimental data with uv-vis spectra obtained ad different times

        returns
        -------
        ax : matplotlib.Axes
            axes with plotted data
        """
        ax.set_title(experiment.sample_name)
        for data_point in experiment.data_points:
            ax.plot(data_point.get_wavelength(), data_point.get_absorbance(), label=data_point.time)
        ax.legend()
        return ax

    def plot_experiments(self, experiments:list[Experiment]):
        """
        plots experimental data from studies of different samples

        parameters
        ----------
        experiments : list[Experiment]
            list of experiments with experimental data
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

    def plot_raw_calibration(self, points, compound):
        """
        plots calibration data, i.e. uv-vis spectra for different concentrations of compound

        parameters
        ----------
        points : list[CalibrationPoint]
            list of calibration points with information about spectra and concentrations
        compound : str
            compound used for calibration
        """
        fig, ax = plt.subplots()
        ax.set_title(compound)
        for point in points:
            ax.plot(point.get_wavelength(), point.get_absorbance(), label=point.get_concentration())
        ax.legend()
        plt.show(block=False)

    def plot_calibration(self, calibration):
        """
        plots results of calibration as uv-vis spectra with vertical line at wavelength used for calibration and absorbance vs. concentration data, experimental and fitted by linear function

        parameters
        ----------
        calibration : Calibration
            calibration with corresponding uv-vis spectra, calibration wavelength and calibration coefficient
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

    def plot_results(self, results:list[Result]):
        """
        plots concentration vs. time plot for different products of phenol photocatalytic oxidation for every sample studied

        parameters
        ----------
        results : list[Result]
            list of results obtained after processing of experimental data
        """
        for result in results:
            points_dict = {}
            for point in result.get_points():
                for name, concentration in zip(point.get_reference_names(), point.get_concentrations()):
                    if name not in points_dict:
                        points_dict[name] = (list(), list())
                    points_dict[name][0].append(point.get_time())
                    points_dict[name][1].append(concentration)
            if len(points_dict) == 1:
                fig, ax = plt.subplots()
                name, xy = points_dict.popitem()
                ax.set_title(name)
                ax.plot(xy[0], xy[1], linestyle='--', marker='.')
            else:
                cols = math.ceil(math.sqrt(len(points_dict)))
                rows = math.ceil(len(points_dict) / cols)
                fig, axs = plt.subplots(nrows=rows, ncols=cols)
                for row in range(rows):
                    for col in range(cols):
                        if not bool(points_dict):
                            break
                        name, xy = points_dict.popitem()
                        axs[row,col].set_title(name)
                        axs[row,col].plot(xy[0], xy[1], linestyle='--', marker='.')
            plt.suptitle(result.get_name())
            plt.show(block=False)

    def plot_result_point(self, datapoint:DataPoint, resultpoint:ResultPoint):
        """
        plots experimental spectrum, reference spectra used for fitting multiplied by corresponding coefficient and sum of reference spectra

        parameters
        ----------
        datapoint : DataPoint
            experimental data point with uv-vis spectrum
        resultpoint : ResultPoint
            result point with reference spectra, coefficients obtained after fitting
        """
        fig, ax = plt.subplots()
        ax.plot(datapoint.get_wavelength(), datapoint.get_absorbance(), label='raw data')
        sum_absorbance = np.full(len(datapoint.get_absorbance()), 0)
        for reference_name, corrected_reference_spectrum in zip(resultpoint.get_reference_names(), resultpoint.get_corrected_reference_spectra()):
            ax.plot(corrected_reference_spectrum.get_wavelength(), corrected_reference_spectrum.get_absorbance(), linestyle='--', label=reference_name)
            sum_absorbance = sum_absorbance + corrected_reference_spectrum.get_absorbance()
        ax.plot(datapoint.get_wavelength(), sum_absorbance, label='sum')
        ax.set_title(f'time = {datapoint.get_time()}')
        ax.set_xlabel('Wavelength, nm')
        ax.set_ylabel('Absorbance')
        ax.legend()
        plt.show(block=False)
