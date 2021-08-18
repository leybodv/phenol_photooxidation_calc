# TODO: docs

from spectrum import Spectrum

class DataPoint():
    """
    """

    def __init__(self, time, wavelength, absorbance):
        """
        """
        print(f'DataPoint().__init__(self, time, wavelength, absorbance') #LOG
        self.time = time
        self.spectrum = Spectrum(wavelength=wavelength, absorbance=absorbance)

    def get_wavelength(self):
        """
        """
        print(f'DataPoint().get_wavelength(self):') #LOG
        return self.spectrum.get_wavelength()

    def get_absorbance(self):
        """
        """
        print(f'DataPoint().get_absorbance(self):') #LOG
        return self.spectrum.get_absorbance()
