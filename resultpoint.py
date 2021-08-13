# TODO: docs

from experiment import Experiment

class ResultPoint():

    def __init__(self, experimental_point, calibrations):
        """
        """
        print(f'ResultPoint().__init__(self, experimental_point, calibrations):') #LOG
        self.time = experimental_point.time
        self.reference_spectra, self.reference_names = self.find_out_spectra(calibrations) # TODO: define method
        self.coefficients = self.find_coefficients(experimental_point.spectrum, self.reference_spectra) # TODO: add spectrum instance variable to Experiment; define method
        self.concentrations = self.find_concentrations(self.coefficients, self.reference_spectra, calibrations) # TODO: define method
