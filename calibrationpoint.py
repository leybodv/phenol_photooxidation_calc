# TODO: docs
# TODO: check access to calibraionpoint.wavelength and calibrationpoint.absorbance variables

from spectrum import Spectrum

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
#        print(f'{self.concentration = }') #LOG
#        print(f'{self.absorbance = }') #LOG
#        print(f'{self.wavelength = }') #LOG
#        print(f'{self.wavelength == wavelength = }') #LOG
#        print(f'{type(wavelength) = }') #LOG
        absorbance = self.absorbance[self.wavelength == wavelength][0]
        return absorbance

    def get_wavelengths(self) -> array:
        """
        """
        print(f'CalibrationPoint().get_wavelengths(self):') #LOG
        return self.spectrum.get_wavelengths() # TODO: define method

    def get_absorbances(self) -> array:
        """
        """
        print(f'CalibrationPoint().get_absorbances(self):') #LOG
        return self.spectrum.get_absorbances() # TODO: define method

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
