# TODO: docs

import numpy as np
from spectrum import Spectrum

class Spectrum():
    """
    """

    def __init__(self, wavelength, absorbance):
        """
        """
        print(f'Spectrum().__init__(self, wavelength, absorbance):') #LOG
        self.wavelength = np.array(wavelength)
        self.absorbance = np.array(absorbance)

    def get_wavelength(self) -> np.ndarray:
        """
        """
        print(f'Spectrum().get_wavelength():') #LOG
        return self.wavelength

    def get_absorbance(self) -> np.ndarray:
        """
        """
        print(f'Spectrum().get_absorbance(self):') #LOG
        return self.absorbance

    def get_absorbance_at(self, wavelength:float) -> float:
        """
        """
        print(f'Spectrum().get_absorbance(self, wavelength):') #LOG
        return self.absorbance[self.wavelength == wavelength][0]

    def truncate(self, x_from:float, x_to:float) -> Spectrum:
        """
        """
        print(f'Spectrum().truncate(self, x_from, x_to)') #LOG
        spectrum = Spectrum(wavelength=self.wavelength[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)], absorbance=self.absorbance[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)])
        return spectrum
