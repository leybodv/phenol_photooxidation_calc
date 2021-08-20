# TODO: docs

from datapoint import DataPoint
from spectrum import Spectrum
import numpy as np
import scipy.optimize as spopt

class ResultPoint():
    """
    class represents single result point with information about time from the beginning of the experiment, reference_spectra used to fit experimental data, reference compounds names, coefficient of fitting and concentrations of corresponding compounds

    class variables
    ---------------
    use_points_from : float (default:190)
        use only points with wavelengths greater or equal to this value for fitting experimental spectrum with reference spectra
    use_points_to : float (default : 450)
        use only points with wavelengths less or equal to this value for fitting experimental spectrum with reference spectra

    instance variables
    ------------------
    time : float
        time from the beginning of the experiment at which specimen was collected for uv-vis analysis
    reference_spectra : list[Spectrum]
        spectra used for fitting of experimental spectrum
    reference_names : list[str]
        names of compounds of corresponding reference_spectra
    coefficients : numpy.ndarray[float]
        coefficients of fitting experimental spectrum by reference spectra
    concentrations : numpy.ndarray[float]
        concentrations of corresponding compounds which reference spectra were used for fitting experimental data
    """

    use_points_from = 190
    use_points_to = 450

    def __init__(self, experimental_point:DataPoint, reference_spectra:list, reference_names:list, calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray):
        """
        assigns parameters to instance variables, calculates fitting coefficients and concentrations of reference compounds

        parameters
        ----------
        experimental_point : DataPoint
            point with experimental data, i.e. time and spectrum
        reference_spectra : list[Spectrum]
            reference spectra used to fit experimental data
        reference_names : list[str]
            reference compounds names
        calibration_coefficients : numpy.ndarray[float]
            coefficients of absorbance vs. concentration calibration for reference compounds
        calibration_wavelengths : numpy.ndarrat[float]
            wavelengths used for absorbance vs. concentration calibration for reference compounds
        """
        self.time = experimental_point.time
        self.reference_spectra = reference_spectra
        self.reference_names = reference_names
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra)
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibration_coefficients, calibration_wavelengths)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list) -> np.ndarray:
        """
        finds coefficients of fitting of experimental spectrum with reference spectra. fitting function is absorbance_fitted = sum(reference_absorbance_i * coefficient_i). coefficients are found by scipy.optimize.least_squares method with bounds from 0 to infinity. only part of spectra from use_points_from to use_points_to is used to reduce influence of baseline data

        parameters
        ----------
        spectrum : Spectrum
            experimental spectrum
        reference_spectra : list[Spectrum]
            reference spectra used for fitting

        returns
        -------
        coefficients : numpy.ndarray
            coefficients obtained after least squares solution
        """
        truncated_spectrum = spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to)
        truncated_reference_spectra = list()
        for reference_spectrum in reference_spectra:
            truncated_reference_spectra.append(reference_spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to))
        coefficients_guess = np.full(len(reference_spectra), 0.5)
        fit_results = spopt.least_squares(self.get_residuals_y, coefficients_guess, bounds=(0, np.inf), loss='linear', args=(truncated_reference_spectra, truncated_spectrum))
        return fit_results.x

    def get_residuals_y(self, coefficients:list[float], reference_spectra:list[Spectrum], experimental_spectrum:Spectrum) -> np.ndarray:
        """
        calculates residuals between calculated and experimental data. used for fitting by scipy.optimize.least_squares method

        parameters
        ----------
        coefficients : list[float]
            coefficients to be found by least squares method
        reference_spectra : list[Spectrum]
            reference spectra used for fitting
        experimental_spectrum : Spectrum
            experimental spectrum to be fitted by least squares

        returns
        -------
        residuals : numpy.ndarray
            residuals between calculated and experimental data
        """
        spectra_sum = np.zeros_like(experimental_spectrum.get_absorbance())
        for coefficient, reference_spectrum in zip(coefficients, reference_spectra):
            spectra_sum = spectra_sum + coefficient * reference_spectrum.get_absorbance()
        residuals = spectra_sum - experimental_spectrum.get_absorbance()
        return residuals


    def find_concentrations(self, coefficients:np.ndarray, reference_spectra:list[Spectrum], calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray) -> np.ndarray:
        """
        finds concentrations of corresponding compounds using coefficient of absorbance vs. concentration calibration

        parameters
        ----------
        coefficients : numpy.ndarray[float]
            coefficients of fitting experimental spectrum with sum of reference spectra
        reference_spectra : list[Spectrum]
            reference spectra used for fitting
        calibration_coefficients : numpy.ndarray[float]
            coefficients of absorbance vs. concentration calibration
        calibration_wavelengths : numpy.ndarray[float]
            wavelengths used for absorbance vs. concentration calibration for corresponding reference compounds

        returns
        -------
        concentrations : numpy.ndarray[float]
            list of concentrations
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
