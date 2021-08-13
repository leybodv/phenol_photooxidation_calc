# TODO: docs

from experiment import Experiment

class ResultPoint():

    def __init__(self, experimental_point, calibrations):
        """
        """
        print(f'ResultPoint().__init__(self, experimental_point, calibrations):') #LOG
        self.time = experimental_point.time
        self.reference_spectra, self.reference_names = self.find_out_spectra(calibrations) # TODO: reference_spectra is list of Spectrum instances, define class
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra) # TODO: add spectrum instance variable to Experiment; define method
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibrations) # TODO: define method

    def find_out_spectra(self, calibrations):
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

    def find_coefficients(self, spectrum, reference_spectra):
        """
        """
        print(f'ResultPoint().find_coefficients(self, spectrum, reference_spectra):') #LOG
