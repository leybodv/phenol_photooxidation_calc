from spectrum import Spectrum
import numpy as np

class DataPoint():
    """
    class represents experimental data point with information about time and uv-vis spectrum

    instance variables
    ------------------
    time : float
        time from the beginning of experiment at which specimen was collected for uv-vis characterization
    spectrum : Spectrum
        experimental uv-vis spectrum of sample
    """

    def __init__(self, time, wavelength, absorbance):
        """
        assigns parameters to instance variables

        parameters
        ----------
        time : float
            time from the beginning of experiment at which specimen was collected for uv-vis characterization
        wavelength : numpy.ndarray[float] or list[float]
            array of wavelengths of uv-vis spectrum
        absorbance : numpy.ndarray[float] or list[float]
            array of absorbances of uv-vis spectrum
        """
        self.time = time
        self.spectrum = Spectrum(wavelength=wavelength, absorbance=absorbance)

    def get_wavelength(self) -> np.ndarray:
        """
        getter to obtain array of wavelengths of uv-vis spectrum

        returns
        -------
        wavelengths : numpy.ndarray[float]
            array of wavelengths of uv-vis spectrum
        """
        return self.spectrum.get_wavelength()

    def get_absorbance(self) -> np.ndarray:
        """
        getter to obtain array of absorbances of uv-vis spectrum

        returns
        -------
        absorbances : numpy.ndarray[float]
            array of absorbances of uv-vis spectrum
        """
        return self.spectrum.get_absorbance()
