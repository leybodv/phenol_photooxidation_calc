# TODO: docs

from plotter import Plotter
from calibration import Calibration
from datapoint import DataPoint
from spectrum import Spectrum
import numpy as np
import scipy.optimize as spopt

class ResultPoint():

    def __init__(self, experimental_point:DataPoint, calibrations:list):
        """
        """
        print(f'ResultPoint().__init__(self, experimental_point, calibrations):') #LOG
        self.time = experimental_point.time
        self.reference_spectra, self.reference_names = self.find_out_spectra(calibrations)
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra)
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibrations)

    def find_out_spectra(self, calibrations:list) -> tuple:
        """
        """
        print(f'ResultPoint().find_out_spectra(self, calibrations):') #LOG
        reference_spectra = list()
        reference_names = list()
        for calibration in calibrations:
            Plotter().plot_raw_calibration(calibration.calibration_points)
            concentration = input('which spectrum to use for fitting data? enter concentration: ')
            reference_spectra.append(calibration.get_spectrum_by_concentration(concentration))
            reference_names.append(calibration.solute)
        return (reference_spectra, reference_names)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list) -> np.ndarray:
        """
        """
        print(f'ResultPoint().find_coefficients(self, spectrum, reference_spectra):') #LOG
        popt, pcov = spopt.curve_fit(lambda x, *params: self.get_fitted_y(x, reference_spectra, params), spectrum.get_wavelength(), spectrum.get_absorbance(), p0=np.full(len(reference_spectra), 1))
        return popt

    def get_fitted_y(self, x:float, reference_spectra:list, coefficients:tuple) -> float:
        """
        """
        print(f'ResultPoint().get_fitted_y(self, x, reference_spectra, coefficients):') #LOG
        ys = list()
        for spectrum in reference_spectra:
            ys.append(spectrum.get_absorbance_at(x))
        y = np.sum(np.array(ys) * np.array(coefficients))
        return y

    def find_concentrations(self, coefficients:np.ndarray, reference_spectra:list, calibrations:list) -> np.ndarray:
        """
        """
        print(f'ResultPoint().find_concentrations(self, coefficients, reference_spectra, calibrations):') #LOG
        concentrations = list()
        for coefficient, spectrum, calibration in zip(coefficients, reference_spectra, calibrations):
            corrected_spectrum = Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance()*coefficient)
            calibration_absorbance = corrected_spectrum.get_absorbance_at(calibration.calibration_wavelength)
            concentrations.append(calibration_absorbance / calibration.calibration_coefficient)
        return np.array(calibrations)

    def get_reference_names(self) -> list:
        """
        """
        print(f'ResultPoint().get_reference_names(self):') #LOG
        return self.reference_names

    def get_time(self) -> float:
        """
        """
        print(f'ResultPoint().get_time(self):') #LOG
        return self.time

    def get_concentrations(self) -> np.ndarray:
        """
        """
        print(f'ResultPoint().get_concentrations(self):') #LOG
        return self.concentrations

    def get_corrected_reference_spectra(self) -> list:
        """
        """
        print(f'ResultPoint().get_corrected_reference_spectra(self):') #LOG
        corrected_spectra = list()
        for spectrum, coefficient in zip(self.reference_spectra, self.coefficients):
            corrected_spectra.append(Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance() * coefficient))
        return corrected_spectra
