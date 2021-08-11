# TODO: docs

import numpy as np

class UvVisParser():

    def parse_calibration_from_file(self, file):
        """
        """
        print(f'UvVisParser().parse_calibration_from_file(self, file):') #LOG
        print(f'Processing {file}')
        concentration = input('Enter concentration of solute [mg/L]: ')
        wavelength, absorbance = np.loadtxt(fname = file, delimiter='\t', unpack=True, encoding='utf-8')
        return (concentration, wavelength, absorbance)
