# TODO: docs

class CalibrationPoint():

    def __init__(self, concentration, wavelength, absorbance):
        """
        """
        print(f'CalibrationPoint().__init__(self, concentration, wavelength, absorbance):') #LOG
        self.concentration = concentration
        self.wavelength = wavelength
        self.absorbance = absorbance

    def get_absorbance_at(self, wavelength):
        """
        """
        print(f'CalibrationPoint().get_absorbance_at(self, wavelength):') #LOG
        absorbance = self.absorbance[self.wavelength == wavelength][0]
        return absorbance
