from pathlib import Path
from uvvisparser import UvVisParser
from calibrationpoint import CalibrationPoint
from spectrum import Spectrum
import scipy.optimize as spopt

class Calibration():
    """
    class represents calibration for single component and contains information about names of solute and solvent, calibration points, wavelength used for calibration coefficient determination and calibration coefficient

    instance variables
    ------------------
    solute : str
        name of solute
    solvent : str
        name of solvent
    calibration_points : list[CalibrataionPoint]
        calibration points for specified solute and solvent
    calibration_wavelength : float
        wavelength used for construction of absorbance vs. concentration plot to determine calibration coefficient
    calibration_coefficient : float
        coefficient in the equation absorbance = coefficient * concentration, which is determined from the calibration data
    """

    def __init__(self, solute, solvent, folder):
        """
        assigns solute and solvent to instance variables, parses calibration data in folder, asks user for wavelength to use for calibration and calculates calibration coefficient

        parameters
        ----------
        solute : str
            name of solute
        solvent : str
            name of solvent
        folder : str or Path
            path to folder with files containing calibration spectra
        """
        from plotter import Plotter
        self.solute = solute
        self.solvent = solvent
        self.calibration_points = self.parse_calibration_data(folder)
        self.calibration_wavelength = self.get_wavelength_from_user(self.calibration_points)
        self.calibration_coefficient = self.find_calibration_coefficient(self.calibration_wavelength, self.calibration_points)
        plotter = Plotter()
        plotter.plot_calibration(self)

    def get_solute(self) -> str:
        """
        getter to obtain solute name

        returns
        -------
        solute : str
            name of solute
        """
        return self.solute

    def get_calibration_wavelength(self) -> float:
        """
        getter to obtain wavelength used for calibration

        returns
        -------
        wavelength : float
            wavelength used for calibration
        """
        return self.calibration_wavelength

    def get_calibration_coefficient(self) -> float:
        """
        getter to obtain calibration coefficient

        returns
        -------
        coefficient : float
            calibration coefficient
        """
        return self.calibration_coefficient

    def parse_calibration_data(self, folder):
        """
        parses files in folder with calibration spectra for specified compound
        data must be in a format <wavelength><tab><absorbance> with single header row

        parameters
        ----------
        folder : str or Path
            folder with files containing calibration spectra

        returns
        -------
        calibration_points : list[CalibrationPoint]
            calibration points for different compounds
        """
        calibration_points = list()
        for file in Path(folder).iterdir():
            if file.is_file():
                concentration, wavelength, absorbance = UvVisParser().parse_calibration_from_file(file)
                calibration_points.append(CalibrationPoint(concentration, wavelength, absorbance))
        return calibration_points

    def find_calibration_coefficient(self, calibration_wavelength, calibration_points):
        """
        finds calibration coefficient using least squares method from calibration data, implemented by scipy.optimize.curve_fit method. calibration coefficient is parameter in an equation absorbance = coefficient * concentration. absorbance value is taken at calibration wavelength

        parameters
        ----------
        calibration_wavelength : float
            wavelength used for calibration
        calibration_points : list[CalibrationPoint]
            points which contain concentrations and calibration spectra

        returns
        -------
        calibration_coefficient : float
            calibration coefficient
        """
        absorbances = list()
        concentrations = list()
        for calibration_point in calibration_points:
            absorbances.append(calibration_point.get_absorbance_at(calibration_wavelength))
            concentrations.append(calibration_point.concentration)
        popt, pcov = spopt.curve_fit(self.linear_func, concentrations, absorbances)
        return popt[0]

    def linear_func(self, x, k):
        """
        calculates value of y from linear equation y = k * x. used by scipy.optimize.curve_fit method for fitting calibration data by linear equation

        parameters
        ----------
        x : float
            independent variable in equation y = k * x
        k : float
            parameter in equation y = k * x

        returns
        -------
        y : float
            value of dependent variable in equation y = k * x
        """
        return k * x

    def get_wavelength_from_user(self, points):
        """
        plots calibration spectra and asks user for wavelength value to use for absorbance - concentration calibration

        parameters
        ----------
        points : list[CalibrationPoint]
            calibration points used to plot data

        returns
        -------
        wavelength : float
            wavelength to be used for calibration
        """
        from plotter import Plotter
        plotter = Plotter()
        plotter.plot_raw_calibration(points, self.get_solute())
        wavelength = input('Wavelength to use for calibration and concentration calculation [nm]: ')
        return float(wavelength)

    def get_spectrum_by_concentration(self, concentration:float) -> Spectrum:
        """
        getter to obtain calibration spectrum corresponding to provided concentration

        parameters
        ----------
        concentration : float
            concentration used for calibration

        returns
        -------
        spectrum : Spectrum or None
            calibration spectrum for corresponding concentration or None if concentration is not in a list of calibration points
        """
        spectrum = None
        for point in self.calibration_points:
            if point.get_concentration() == concentration:
                spectrum = point.get_spectrum()
        return spectrum
