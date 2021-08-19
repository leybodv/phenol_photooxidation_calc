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
