# TODO: docs

from spectrum import Spectrum

class DataPoint():
    """
    """

    def __init__(self, time, wavelength, absorbance):
        self.time = time
        self.spectrum = Spectrum(wavelength=wavelength, absorbance=absorbance)
        print(f'DataPoint().__init__(self, time, wavelength, absorbance):') #LOG
        print(f'{self.time = }') #LOG
