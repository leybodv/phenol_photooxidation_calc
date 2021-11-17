import numpy as np

class Spectrum():
    """
    wrapper class for uv-vis spectrum data

    instance variables
    ------------------
    wavelength : numpy.ndarray[float]
        array of wavelengths
    absorbance : numpy.ndarray[float]
        array of absorbances
    """

    def __init__(self, wavelength, absorbance):
        """
        assigns parameters to instance variables

        parameters
        ----------
        wavelength : list[float] or numpy.ndarray[float]
            list of wavelengths
        absorbance : list[float] or numpy.ndarray[float]
            list of absorbances
        """
        self.wavelength = np.array(wavelength)
        self.absorbance = np.array(absorbance)

    def __repr__(self):
        """
        returns string representation of spectrum as <wavelength><tab><absorbance> pairs

        returns
        -------
            string : str
                string representation of spectrum
        """
        string = ''
        for w, a in zip(self.wavelength, self.absorbance):
            string = string + w + '\t' + a + '\n'
        return string

    def get_wavelength(self) -> np.ndarray:
        """
        getter to obtain wavelengths

        returns
        -------
            wavelength : numpy.ndarray[float]
                array of wavelengths
        """
        return self.wavelength

    def get_absorbance(self) -> np.ndarray:
        """
        getter to obtain absorbances

        returns
        -------
        absorbance : numpy.ndarray[float]
            array of absorbances
        """
        return self.absorbance

    def get_absorbance_at(self, wavelength:float) -> float:
        """
        getter to obtain absorbance value at the specified wavelength

        parameters
        ----------
        wavelength : float
            wavelength to search absorbance value

        returns
        -------
        absorbance : float
            value of absorbance at specified wavelength
        """
        return self.absorbance[self.wavelength == wavelength][0]

    def truncate(self, x_from:float, x_to:float) -> 'Spectrum':
        """
        method to reduce spectrum data to specified wavelength interval inclusively

        parameters
        ----------
        x_from, x_to : float
            interval to use for new spectrum construction

        returns
        -------
        spectrum : Spectrum
            spectrum with wavelength in interval [x_from, x_to]
        """
        spectrum = Spectrum(wavelength=self.wavelength[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)], absorbance=self.absorbance[np.logical_and(self.wavelength >= x_from, self.wavelength <= x_to)])
        return spectrum
