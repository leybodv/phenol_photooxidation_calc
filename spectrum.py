# TODO: docs

import numpy as np

class Spectrum():
    """
    """

    def __init__(self, wavelength, absorbance):
        """
        """
        self.wavelength = np.array(wavelength)
        self.absorbance = np.array(absorbance)

    def get_wavelength(self) -> np.ndarray:
        """
        """
        return self.wavelength

    def get_absorbance(self) -> np.ndarray:
        """
        """
        return self.absorbance

    def get_absorbance_at(self, wavelength:float) -> float:
        """
        """
        return self.absorbance[self.wavelength == wavelength][0]

    def truncate(self, x_from:float, x_to:float) -> 'Spectrum':
        """
        """
        spectrum = Spectrum(wavelength=self.wavelength[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)], absorbance=self.absorbance[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)])
        return spectrum
