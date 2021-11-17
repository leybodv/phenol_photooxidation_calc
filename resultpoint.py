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

    def __init__(self, experimental_point:DataPoint, reference_spectra:list, reference_names:list, calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray, phenol_init_conc:float, peroxide_init_conc:float):
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
        calibration_wavelengths : numpy.ndarray[float]
            wavelengths used for absorbance vs. concentration calibration for reference compounds
        phenol_init_conc : float
            initial concentration of phenol in μM
        peroxide_init_conc : float
            initial concentration of h2o2 in μM
        """
        self.time = experimental_point.time
        self.reference_spectra = reference_spectra
        self.reference_names = reference_names
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra, reference_names, calibration_coefficients, calibration_wavelengths, phenol_init_conc, peroxide_init_conc)
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibration_coefficients, calibration_wavelengths)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list[Spectrum], reference_names:list[str], conc_calibration_coefficients:np.ndarray, calibration_wavelengths:np.ndarray, phenol_init_conc:float, peroxide_init_conc:float) -> np.ndarray:
        """
        finds coefficients of fitting of experimental spectrum with reference spectra. fitting function is absorbance_fitted = sum(reference_absorbance_i * coefficient_i). coefficients are found by scipy.optimize.least_squares method with bounds from 0 to infinity. only part of spectra from use_points_from to use_points_to is used to reduce influence of baseline data

        parameters
        ----------
        spectrum : Spectrum
            experimental spectrum
        reference_spectra : list[Spectrum]
            reference spectra used for fitting
        reference_names : list[str]
            reference compounds names, order must match corresponding reference_spectra
        conc_calibration_coefficients : numpy.ndarray[float]
            list of concentration calibration coefficients for corresponding compounds
        calibration_wavelengths : numpy.ndarray[float]
            list of calibration wavelengths for corresponding reference compounds
        phenol_init_conc : float
            initial concentration of phenol solution in μM
        peroxide_init_conc : float
            initial concentration of h2o2 solution in μM

        returns
        -------
        coefficients : numpy.ndarray
            coefficients obtained after least squares solution
        """
        truncated_spectrum = spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to)
        truncated_reference_spectra = list()
        for reference_spectrum in reference_spectra:
            truncated_reference_spectra.append(reference_spectrum.truncate(x_from=self.use_points_from, x_to=self.use_points_to))
        coefficients_guess = list()
        bounds_low = list()
        bounds_high = list()
        for reference_spectrum, ref_compound, conc_calibration_coef, calibration_wavelength in zip(reference_spectra, reference_names, conc_calibration_coefficients, calibration_wavelengths):
            bl = 0
            if self.get_time() == 0:
                if ref_compound == 'phenol':
                    bh = phenol_init_conc * conc_calibration_coef / reference_spectrum.get_absorbance_at(calibration_wavelength)
                elif ref_compound == 'h2o2':
                    if peroxide_init_conc == 0:
                        bh = 10 ** (-9)
                    else:
                        bh = peroxide_init_conc * conc_calibration_coef / reference_spectrum.get_absorbance_at(calibration_wavelength)
                elif ref_compound in ['benzoquinone', 'catechol', 'hydroquinone', 'formic-acid']:
                    bh = 10 ** (-9)
                else:
                    bh = np.inf
            else:
                if ref_compound in ['phenol', 'benzoquinone', 'catechol', 'hydroquinone']:
                    bh = phenol_init_conc * conc_calibration_coef / reference_spectrum.get_absorbance_at(calibration_wavelength)
                elif ref_compound == 'formic-acid':
                    bh = 6 * phenol_init_conc * conc_calibration_coef / reference_spectrum.get_absorbance_at(calibration_wavelength)
                elif ref_compound == 'h2o2':
                    bh = np.inf
                else:
                    bh = np.inf
            if np.isinf(bl) or np.isinf(bh):
                coefficients_guess.append(peroxide_init_conc * conc_calibration_coef / reference_spectrum.get_absorbance_at(calibration_wavelength))
            else:
                coefficients_guess.append((bl + bh) / 2)
            bounds_low.append(bl)
            bounds_high.append(bh)
        fit_results = spopt.least_squares(self.get_residuals_y, coefficients_guess, bounds=(bounds_low, bounds_high), loss='cauchy', f_scale=0.1, args=(truncated_reference_spectra, truncated_spectrum))
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
            print(f'{len(experimental_spectrum.get_absorbance()) = }') # LOG
            print(f'{len(reference_spectrum.get_absorbance()) = }') # LOG
            print(f'{experimental_spectrum = }')
            print(f'{reference_spectrum = }')
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
            concentration = calibration_absorbance / calibration_coefficient
            concentrations.append(concentration)
        return np.array(concentrations)

    def get_reference_names(self) -> list:
        """
        getter to obtain reference compounds names

        returns
        -------
        reference_names : list[Spectrum]
            reference compounds names
        """
        return self.reference_names

    def get_time(self) -> float:
        """
        getter to obtain time from the beginning of experiment

        returns
        -------
        time : float
            time from the beginning of experiment
        """
        return self.time

    def get_concentrations(self) -> np.ndarray:
        """
        getter to obtain concentrations of phenol oxidation products

        returns
        -------
        concentrations : numpy.ndarray[float]
            concentrations of phenol oxidation products
        """
        return self.concentrations

    def get_corrected_reference_spectra(self) -> list:
        """
        calculates reference spectra with absorbances multiplied by corresponding fitting coefficients

        returns
        -------
        corrected_spectra : list[Spectrum]
            reference spectra with absorbances multiplied by corresponding fitting coefficients
        """
        corrected_spectra = list()
        for spectrum, coefficient in zip(self.reference_spectra, self.coefficients):
            corrected_spectra.append(Spectrum(wavelength=spectrum.get_wavelength(), absorbance=spectrum.get_absorbance() * coefficient))
        return corrected_spectra
