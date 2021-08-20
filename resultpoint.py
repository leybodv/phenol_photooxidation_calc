# TODO: docs

from datapoint import DataPoint
from spectrum import Spectrum
import numpy as np
import scipy.optimize as spopt

class ResultPoint():

    use_points_from = 190
    use_points_to = 450

    def __init__(self, experimental_point:DataPoint, reference_spectra:list, reference_names:list, calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray):
        """
        """
        self.time = experimental_point.time
        self.reference_spectra = reference_spectra
        self.reference_names = reference_names
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra)
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibration_coefficients, calibration_wavelengths)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list) -> np.ndarray:
        """
        """
        truncated_spectrum = spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to)
        truncated_reference_spectra = list()
        for reference_spectrum in reference_spectra:
            truncated_reference_spectra.append(reference_spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to))
        coefficients_guess = np.full(len(reference_spectra), 0.5)
        fit_results = spopt.least_squares(self.get_residuals_y, coefficients_guess, bounds=(0, np.inf), loss='linear', args=(truncated_reference_spectra, truncated_spectrum))
        return fit_results.x

    def get_fitted_y(self, x:float, reference_spectra:list, coefficients:tuple) -> float:
        """
        """
        ys = list()
        for spectrum in reference_spectra:
            ys.append(spectrum.get_absorbance_at(x))
        y = np.sum(np.array(ys) * np.array(coefficients))
        return y

    def get_residuals_y(self, coefficients:list[float], reference_spectra:list[Spectrum], experimental_spectrum:Spectrum) -> np.ndarray:
        """
        """
        spectra_sum = np.zeros_like(experimental_spectrum.get_absorbance())
        for coefficient, reference_spectrum in zip(coefficients, reference_spectra):
            spectra_sum = spectra_sum + coefficient * reference_spectrum.get_absorbance()
        residuals = spectra_sum - experimental_spectrum.get_absorbance()
        return residuals


    def find_concentrations(self, coefficients:np.ndarray, reference_spectra:list[Spectrum], calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray) -> np.ndarray:
        """
        """
        concentrations = list()
        for coefficient, spectrum, calibration_coefficient, calibration_wavelength in zip(coefficients, reference_spectra, calibration_coefficients, calibration_wavelengths):
            corrected_spectrum = Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance()*coefficient)
            calibration_absorbance = corrected_spectrum.get_absorbance_at(calibration_wavelength)
            concentrations.append(calibration_absorbance / calibration_coefficient)
        return np.array(concentrations)

    def get_reference_names(self) -> list:
        """
        """
        return self.reference_names

    def get_time(self) -> float:
        """
        """
        return self.time

    def get_concentrations(self) -> np.ndarray:
        """
        """
        return self.concentrations

    def get_corrected_reference_spectra(self) -> list:
        """
        """
        corrected_spectra = list()
        for spectrum, coefficient in zip(self.reference_spectra, self.coefficients):
            corrected_spectra.append(Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance() * coefficient))
        return corrected_spectra
