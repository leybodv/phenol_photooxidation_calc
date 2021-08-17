# TODO: docs

from pathlib import Path
from uvvisparser import UvVisParser
from calibrationpoint import CalibrationPoint
from plotter import Plotter
import scipy.optimize as spopt

class Calibration():

    def __init__(self, solute, solvent, folder):
        """
        """
        print(f'__init__(self, solute, solvent, folder):') #LOG
        self.solute = solute
        self.solvent = solvent
        self.calibration_points = self.parse_calibration_data(folder)
        self.calibration_wavelength = self.get_wavelength_from_user(self.calibration_points)
        self.calibration_coefficient = self.find_calibration_coefficient(self.calibration_wavelength, self.calibration_points)
        plotter = Plotter()
        plotter.plot_calibration(self)

    def parse_calibration_data(self, folder):
        """
        """
        print(f'parse_calibration_data(self, folder):') #LOG
        calibration_points = list()
        for file in Path(folder).iterdir():
            if file.is_file():
                concentration, wavelength, absorbance = UvVisParser().parse_calibration_from_file(file)
                calibration_points.append(CalibrationPoint(concentration, wavelength, absorbance))
        return calibration_points

    def find_calibration_coefficient(self, calibration_wavelength, calibration_points):
        """
        """
        print(f'find_calibration_coefficient(self, calibration_wavelength, calibration_points):') #LOG
        absorbances = list()
        concentrations = list()
        for calibration_point in calibration_points:
            absorbances.append(calibration_point.get_absorbance_at(calibration_wavelength))
            concentrations.append(calibration_point.concentration)
        popt, pcov = spopt.curve_fit(self.linear_func, concentrations, absorbances)
        return popt[0]

    def linear_func(self, x, k):
        """
        """
        return k * x

    def get_wavelength_from_user(self, points):
        """
        """
        plotter = Plotter()
        plotter.plot_raw_calibration(points)
        wavelength = input('Wavelength to use for calibration and concentration calculation [nm]: ')
        return float(wavelength)

    def get_spectrum_by_concentration(self, concentration:float) -> Spectrum:
        """
        """
        print(f'Calibration().get_spectrum_by_concentration(self, concentration)') #LOG
        spectrum = None
        for point in self.calibration_points:
            if point.get_concentration() == concentration: #TODO: define method
                spectrum = point.get_spectrum() #TODO define method
        return spectrum
