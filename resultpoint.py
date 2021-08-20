# TODO: docs

from datapoint import DataPoint
from spectrum import Spectrum
import numpy as np
import scipy.optimize as spopt

class ResultPoint():

    mask_points_from = 450

    def __init__(self, experimental_point:DataPoint, reference_spectra:list, reference_names:list, calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray):
        """
        """
        print(f'ResultPoint().__init__(self, experimental_point, calibrations):') #LOG
        self.time = experimental_point.time
        self.reference_spectra = reference_spectra
        self.reference_names = reference_names
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra)
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibration_coefficients, calibration_wavelengths)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list) -> np.ndarray:
        """
        """
        print(f'ResultPoint().find_coefficients(self, spectrum, reference_spectra):') #LOG
        truncated_spectrum = spectrum.truncate(self.mask_points_from, np.inf)
        truncated_reference_spectra = list()
        for reference_spectrum in reference_spectra:
            truncated_reference_spectra.append(reference_spectrum.truncate(self.mask_points_from, np.inf))
        popt, pcov = spopt.curve_fit(lambda x, *params: self.get_fitted_y(x, truncated_reference_spectra, params), truncated_spectrum.get_wavelength(), truncated_spectrum.get_absorbance(), p0=np.full(len(reference_spectra), 0.5), bounds=(0, np.inf))
#        popt, pcov = spopt.curve_fit(lambda x, *params: self.get_fitted_y(x, truncated_reference_spectra, params), truncated_spectrum.get_wavelength(), truncated_spectrum.get_absorbance(), p0=np.full(len(reference_spectra), 0.5), bounds=(0, np.inf), sigma=1/truncated_spectrum.get_absorbance())
        print(f'{popt = }') #LOG
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

    def find_concentrations(self, coefficients:np.ndarray, reference_spectra:list, calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray) -> np.ndarray:
        """
        """
        print(f'ResultPoint().find_concentrations(self, coefficients, reference_spectra, calibrations):') #LOG
        concentrations = list()
        for coefficient, spectrum, calibration_coefficient, calibration_wavelength in zip(coefficients, reference_spectra, calibration_coefficients, calibration_wavelengths):
            corrected_spectrum = Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance()*coefficient)
            calibration_absorbance = corrected_spectrum.get_absorbance_at(calibration_wavelength)
            concentrations.append(calibration_absorbance / calibration_coefficient)
        return np.array(concentrations)

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
