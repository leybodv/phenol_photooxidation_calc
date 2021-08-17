# TODO: docs
# TODO: check imports

from experiment import Experiment

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
            Plotter().plot_raw_calibration(calibration.calibration_points) #TODO: import Plotter, Calibration
            concentration = input('which spectrum to use for fitting data? enter concentration: ')
            reference_spectra.append(calibration.get_spectrum_by_concentration(concentration)) # TODO: add method to Calibration
            reference_names.append(calibration.solute)
        return (reference_spectra, reference_names)

    def find_coefficients(self, spectrum:Spectrum, reference_spectra:list) -> array: # TODO: define Spectrum class
        """
        """
        print(f'ResultPoint().find_coefficients(self, spectrum, reference_spectra):') #LOG
        popt, pcov = spopt.curve_fit(lambda x, params*: self.get_fitted_y(x, reference_spectra, params), spectrum.wavelength, spectrum.absorbance, p0=np.full(len(reference_spectra), 1)) # TODO: define method get_fitted_y, add wavelength and absorbance instance variables to Spectrum class
        return popt

    def get_fitted_y(self, x:float, reference_spectra:list, coefficients:list) -> float:
        """
        """
        print(f'ResultPoint().get_fitted_y(self, x, reference_spectra, coefficients):') #LOG
        ys = list()
        for spectrum in reference_spectra:
            ys.append(spectrum.get_absorbance_at(x)) # TODO: define method in Spectrum class
        y = np.sum(np.array(ys) * np.array(coefficients)) # TODO: import numpy

    def find_concentrations(self, coefficients:array, reference_spectra:list, calibrations:list) -> array:
        """
        """
        print(f'ResultPoint().find_concentrations(self, coefficients, reference_spectra, calibrations):') #LOG
        concentrations = list()
        for coefficient, spectrum, calibration in zip(coefficients, reference_spectra, calibrations):
            corrected_spectrum = Spectrum(wavelength=spectrum.wavelength, absorbance=spectrum.absorbance*coefficient)
            calibration_absorbance = corrected_spectrum.get_absorbance_at(calibration.calibration_wavelength)
            concentrations.append(calibration_absorbance / calibration.calibration_coefficient)
        return np.array(calibrations) # TODO: import numpy
