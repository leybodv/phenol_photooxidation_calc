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
