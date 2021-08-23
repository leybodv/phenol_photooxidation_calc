import numpy as np

class UvVisParser():
    """
    utility class for parsing uv-vis data
    """

    def parse_calibration_from_file(self, file):
        """
        ask user for concentration used for calibration and parse corresponding uv-vis spectrum

        parameters
        ----------
        file : str or Path
            file with calibration spectrum data

        returns
        -------
        concentration : float
            concentration used for calibration
        wavelength : numpy.ndarray[float]
            array of wavelengths parsed from file
        absorbance : numpy.ndarray[float]
            array of absorbances parsed from file
        """
        concentration = input(f'Importing file {file}. Enter concentration of solute [mmol/L]: ')
        concentration = float(concentration)
        wavelength, absorbance = np.loadtxt(fname = file, delimiter='\t', unpack=True, encoding='utf-8', skiprows=1)
        if np.any(absorbance < 0):
            absorbance = absorbance + abs(absorbance.min())
        return (concentration, wavelength, absorbance)
