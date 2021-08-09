# TODO: docs

from pathlib import Path
from uv_vis_parser import UvVisParser # TODO: make class
from calibrationpoint import CalibrationPoint # TODO: make class
import scipy.optimize as spopt

class Calibration():

    def __init__(self, solute, solvent, calibration_wavelength, calibration_folder): # TODO: add parameter to method invocation in PhPhOx_Shell
        """
        """
        print(f'__init__(self, solute, solvent, calibration_wavelength, calibration_folder):') #LOG
        self.solute = solute
        self.solvent = solvent
        self.calibration_wavelength = calibration_wavelength
        self.calibration_points = self.parse_calibration_data(calibration_folder)
        self.calibration_coefficient = self.find_calibration_coefficient(calibration_wavelength, calibration_points)

    def parse_calibration_data(self, calibration_folder):
        """
        """
        print(f'parse_calibration_data(self, calibration_folder):') #LOG
        calibration_points = list()
        for file in Path(calibration_folder):
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
            absorbances.append(calibration_point.get_absorbance_at(calibration_wavelength)) # TODO: add method to class CalibrationPoint 
            concentrations.append(calibration_point.concentration)
        popt, pcov = spopt.curve_fit(self.linear_func, concentrations, absorbances)
        return popt[0]

    def linear_func(self, x, k):
        """
        """
        return k * x
