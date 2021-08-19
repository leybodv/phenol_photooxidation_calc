# TODO: docs

import numpy as np

class UvVisParser():

    def parse_calibration_from_file(self, file):
        """
        """
        print(f'UvVisParser().parse_calibration_from_file(self, file):') #LOG
        concentration = input(f'Importing file {file}. Enter concentration of solute [mmol/L]: ')
        concentration = float(concentration)
        wavelength, absorbance = np.loadtxt(fname = file, delimiter='\t', unpack=True, encoding='utf-8', skiprows=1)
        return (concentration, wavelength, absorbance)
