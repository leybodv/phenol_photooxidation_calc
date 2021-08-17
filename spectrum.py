# TODO: docs

import numpy as np

class Spectrum():
    """
    """

    def __init__(self, wavelength, absorbance):
        """
        """
        print(f'Spectrum().__init__(self, wavelength, absorbance):') #LOG
        self.wavelength = np.array(wavelength)
        self.absorbance = np.array(absorbance)

    def get_wavelength(self) -> array:
        """
        """
        print(f'Spectrum().get_wavelength():') #LOG
        return self.wavelength

    def get_absorbance(self) -> array:
        """
        """
        print(f'Spectrum().get_absorbance(self):') #LOG
        return self absorbance
