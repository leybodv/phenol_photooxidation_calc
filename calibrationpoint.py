# TODO: docs

from spectrum import Spectrum
import numpy as np

class CalibrationPoint():

    def __init__(self, concentration, wavelength, absorbance):
        """
        """
        print(f'CalibrationPoint().__init__(self, concentration, wavelength, absorbance):') #LOG
        self.concentration = concentration
        self.spectrum = Spectrum(wavelength=wavelength, absorbance=absorbance)

    def get_absorbance_at(self, wavelength):
        """
        """
        print(f'CalibrationPoint().get_absorbance_at(self, wavelength):') #LOG
        absorbance = self.spectrum.get_absorbance_at(wavelength)
        return absorbance

    def get_wavelength(self) -> np.ndarray:
        """
        """
        print(f'CalibrationPoint().get_wavelength(self):') #LOG
        return self.spectrum.get_wavelength() # TODO: define method

    def get_absorbance(self) -> np.ndarray:
        """
        """
        print(f'CalibrationPoint().get_absorbance(self):') #LOG
        return self.spectrum.get_absorbance()

    def get_concentration(self) -> float:
        """
        """
        print(f'CalibrationPoint().get_concentration(self):') #LOG
        return self.concentration

    def get_spectrum(self) -> Spectrum:
        """
        """
        print(f'CalibrationPoint().get_spectrum(self)') #LOG
        return self.spectrum
