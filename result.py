# TODO: docs

from experiment import Experiment
from resultpoint import ResultPoint
from datapoint import DataPoint
from calibration import Calibration
import numpy as np

class Result():

    def __init__(self, experiment:Experiment, calibrations:list, verbose=False):
        """
        """
        print(f'Result().__init__(self, experiment, calibrations)') #LOG
        self.sample_name = experiment.sample_name
        self.result_points = self.calculate_results(experiment.data_points, calibrations, verbose)

    def calculate_results(self, raw_data_points:list[DataPoint], calibrations:list[Calibration], verbose:bool):
        """
        """
        print(f'Result().calculate_results(self, raw_data_points, calibrations)') #LOG
        from plotter import Plotter
        result_points = list()
        calibration_wavelengths = list()
        calibration_coefficients = list()
        for calibration in calibrations:
            calibration_wavelengths.append(calibration.get_calibration_wavelength())
            calibration_coefficients.append(calibration.get_calibration_coefficient())
        calibration_wavelengths = np.array(calibration_wavelengths)
        calibration_coefficients = np.array(calibration_coefficients)
        reference_spectra, reference_names = self.find_out_spectra(calibrations)
        for point in raw_data_points:
            resultpoint = ResultPoint(experimental_point=point, reference_spectra=reference_spectra, reference_names=reference_names, calibration_coefficients=calibration_coefficients, calibration_wavelengths=calibration_wavelengths)
            result_points.append(resultpoint)
            if verbose:
                Plotter().plot_result_point(point, resultpoint)
        return result_points

    def get_name(self) -> str:
        """
        """
        print(f'Result().get_name(self):') #LOG
        return self.sample_name

    def get_points(self) -> list:
        """
        """
        print(f'Result().get_points(self):') #LOG
        return self.result_points

    def find_out_spectra(self, calibrations:list[Calibration]) -> tuple:
        """
        """
        print(f'ResultPoint().find_out_spectra(self, calibrations):') #LOG
        from plotter import Plotter
        reference_spectra = list()
        reference_names = list()
        for calibration in calibrations:
            Plotter().plot_raw_calibration(calibration.calibration_points, calibration.get_solute())
            concentration = input('which spectrum to use for fitting data? enter concentration: ')
            concentration = float(concentration)
            reference_spectra.append(calibration.get_spectrum_by_concentration(concentration))
            reference_names.append(calibration.get_solute())
        return (reference_spectra, reference_names)
